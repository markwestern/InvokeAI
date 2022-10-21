function toBase64(file) {
    return new Promise((resolve, reject) => {
        const r = new FileReader();
        r.readAsDataURL(file);
        r.onload = () => resolve(r.result);
        r.onerror = (error) => reject(error);
    });
}

function appendOutput(src, srcUpscaled, seed, config) {


    const variations = config.variation_amount > 0
        ? (
            config.with_variations
                ? config.with_variations + ','
                : ''
        ) + seed + ':' + config.variation_amount
        : config.with_variations;

    const baseseed = (config.with_variations || config.variation_amount > 0) ? config.seed : seed;

    const dataCaptionItems = {
        Prompt: config.prompt,
        "Seed / Variations": `${baseseed} / ${variations}`,
        "Steps / Scale / Sampler": `${config.steps} / ${config.cfg_scale} / ${config.sampler_name}`,
        "Source Image/Strength": `${config.initimg} / ${config.strength}`
    }
    const dataCaption = Object.keys(dataCaptionItems)
        .filter(key => dataCaptionItems[key])
        .map(key => `<li class="list-group-item"><div class="row"><div class="col-2 text-nowrap">${key}:</div><div class="col">${dataCaptionItems[key]}</div></div></li>`).join('');

    const figureContents = `
    
        <div class='col'>
            <a href='${srcUpscaled || src}' data-fancybox='gallery' data-caption='<ul class="list-group">${dataCaption}</ul>'>
                <img src='${src}'
                    alt='${config.prompt}'
                    title='${config.prompt}'
                    loading='lazy'
                    width='256'
                    height='256'>
            </a>
            <figcaption id='figcaption-${seed}'>${config.prompt}</figcaption>
        </div>
   
    `;

    const outputNode = jQuery('<figure></figure>');
    outputNode.html(figureContents);
    jQuery('#results').prepend(outputNode);

    // Reload image config
    jQuery(`#figcaption-${seed}`).on('click', (e) => {
        jQuery('#generate-form input, select, textarea').each((index, input) => {
            console.log(input)
            if (input.type !== 'file' && config[input.id]) {
                const val = isNaN(config[input.id]) ? config[input.id] : parseFloat(config[input.id]).toString(10);
                console.log(input.id, val)
                jQuery(`#${input.id}`).val(val);
            }
        });


        jQuery('#seed').val(baseseed);
        jQuery('#with_variations').val(variations || '');
        if (jQuery('#variation_amount').val() <= 0) {
            jQuery('#variation_amount').val(0.2);
        }

        saveFields();
    });


}

function saveFields() {
    jQuery('#generate-form input, select, textarea').each((index, input) => {
        if (typeof input.value !== 'object') // Don't save 'file' type
            localStorage.setItem(input.id, input.value);
    });
}

function loadFields() {
    jQuery('#generate-form input, select, textarea').each((index, input) => {
        if (input.type !== 'file') {
            const item = localStorage.getItem(input.id);
            item !== null & typeof item !== 'undefined' && jQuery(`#${input.id}`).val(item);
        }
    });
}

function clearFields(form) {
    localStorage.clear();
    const prompt = jQuery('#prompt').val();
    jQuery('#generate-form').trigger("reset");
    jQuery('#prompt').val(prompt);
}

const BLANK_IMAGE_URL = 'data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg"/>';
async function generateSubmit(form) {
    const prompt = jQuery('#prompt').val();

    // Convert file data to base64
    const formData = Object.fromEntries(new FormData(form));
    formData.initimg_name = formData.initimg.name
    formData.initimg = formData.initimg.name !== '' ? await toBase64(formData.initimg) : null;

    const strength = formData.strength;
    const totalSteps = formData.initimg ? Math.floor(strength * formData.steps) : formData.steps;

    const progressSectionEle = jQuery('#progress-section');
    progressSectionEle.show();
    const progressEle = jQuery('#progress-bar');
    const progressImageEle = jQuery('#progress-image');
    progressImageEle.src = BLANK_IMAGE_URL;

    if (jQuery('#progress_images').is(':checked'))
        progressImageEle.show();
    else
        progressImageEle.hide();

    // Post as JSON, using Fetch streaming to get results
    fetch(form.action, {
        method: form.method,
        body: JSON.stringify(formData),
    }).then(async (response) => {
        const reader = response.body.getReader();

        let noOutputs = true;
        while (true) {
            let { value, done } = await reader.read();
            value = new TextDecoder().decode(value);
            if (done) {
                progressSectionEle.hide();
                break;
            }

            for (let event of value.split('\n').filter(e => e !== '')) {
                const data = JSON.parse(event);
                console.log(data)
                if (data.event === 'result') {
                    noOutputs = false;
                    appendOutput(data.url, data.urlUpscaled, data.seed, data.config);
                    progressEle.width('0%');
                    progressEle.text('0%');

                }
                else if (data.event === 'upscaling-started') {
                    jQuery('processing_cnt').text(data.processed_file_cnt);
                    jQuery('scaling-inprocess-message').show();
                }
                else if (data.event === 'upscaling-done')
                    jQuery('scaling-inprocess-message').hide();
                else if (data.event === 'step') {
                    const percent = (100 * (data.step / totalSteps)).toFixed(0) + '%'
                    progressEle.width(percent);
                    progressEle.text(percent);
                    if (data.url)
                        jQuery('#progress-image').attr('src', data.url);
                }
                else if (data.event === 'canceled') // avoid alerting as if this were an error case
                    noOutputs = false;
            }
        }

        // Re-enable form, remove no-results-message
        jQuery('fieldset').removeAttr('disabled');
        jQuery('#prompt').val(prompt);


        if (noOutputs)
            alert('Error occurred while generating.');
    });

    // Disable form while generating
    jQuery('fieldset').attr('disabled', 'disabled');
    jQuery('#prompt').val(`Generating: '${prompt}'`);
}

async function fetchRunLog() {
    try {
        let response = await fetch('/run_log.json')
        const data = await response.json();
        console.log(data)
        for (let item of data.run_log)
            appendOutput(item.url, item.urlUpscaled, item.seed, item);
    } catch (e) {
        console.error(e);
    }
}

jQuery(document).ready(async () => {
    jQuery('#progress-section').hide();
    jQuery('#scaling-inprocess-message').hide();

    jQuery('#prompt').on('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey)
            generateSubmit(e.target.form);
    });

    jQuery('#generate-form').on('submit', (e) => {
        e.preventDefault();
        generateSubmit(e.target);
    });

    jQuery('#generate-form').on('change', (e) => saveFields(e.target.form));

    jQuery('#reset-seed').on('click', (e) => {
        jQuery('#seed').val(-1);
        saveFields(e.target.form);
    });

    jQuery('#reset-all').on('click', (e) => clearFields(e.target.form));

    jQuery('#remove-image').on('click', (e) => {
        initimg.value = null;
    });

    loadFields();

    jQuery('#cancel-button')
        .on('click', () => fetch('/cancel')
            .catch(e => console.error(e)));

    jQuery(document.documentElement).on('keydown', (e) => {
        if (e.key === 'Escape')
            fetch('/cancel').catch(err => console.error(err));
    });

    if (!config.gfpgan_model_exists)
        jQuery('#gfpgan').hide();

    await fetchRunLog()
})

