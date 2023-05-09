const ALLOWED_TYPES = [
    'image/png',
    'image/gif',
    'image/jpeg',
    'text/plain'
]

function uploadFile() {
    const data = validate()
    if (!data) return

    let formData = new FormData(document.getElementById('form'))
    fetch(`/api/v1/upload?name=${data.filename}&filetype=${data.file.type}`, {
        method: 'POST',
        body: formData,
        headers: { authorization: data.apiKey }
    })
        .then(async (response) => {
            const json = await response.json()
            if (response.status >= 300) {
                return setError(json.detail)
            }
            successfulSend(
                `<span>File was uploaded successful. <a href="/${json.filename}" class="image-url">File url</a></span>`
            )
        })
}

function deleteFile() {
    const data = validate(true)
    if (!data) return

    fetch(`/api/v1/delete?name=${data.filename}`, {
        method: 'DELETE',
        headers: { authorization: data.apiKey }
    })
        .then(async function (response) {
            if (response.status >= 300) {
                return setError((await response.json()).detail)
            }
            successfulSend('Specified file was deleted successful')
        })
}

function validate (deleteMode=false) {
    let file
    if (!deleteMode) {
        const files = document.getElementById('fileInput').files
        if (files.length <= 0) {
            return setError('You don\'t provide a file')
        }

        file = files[0]
        if (!ALLOWED_TYPES.includes(file.type)) {
            return setError('This file type is not allowed')
        }
    }

    const inputFilenameValue = document.getElementById('inputFilename').value
    if (!inputFilenameValue) {
        return setError('Provide a filename')
    }

    if (inputFilenameValue.length > 32) {
        return setError('Too long filename. Over 32 chars')
    }

    const inputApiKeyValue = document.getElementById('inputApiKey').value
    if (!inputApiKeyValue) {
        return setError('Provide an api key')
    }

    return {
        apiKey: inputApiKeyValue,
        filename: inputFilenameValue,
        file
    }
}

function setError (text) {
    const errorAlert = document.getElementById('errorAlert')
    document.getElementById('successfulAlert').classList.add('hidden')
    errorAlert.classList.remove('hidden')
    errorAlert.innerText = text
}

function successfulSend (text) {
    const successfulAlert = document.getElementById('successfulAlert')
    document.getElementById('errorAlert').classList.add('hidden')
    successfulAlert.classList.remove('hidden')
    successfulAlert.innerHTML = text
}

function changeLabelForLabel (input) {
    document.getElementById('labelForLabel').innerText = input.files.length
}

document.getElementById('fileInput').addEventListener(
    'change', event => changeLabelForLabel(event.target)
)