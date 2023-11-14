$(document).ready(() => {
    const sectionStart = $('#sectionStart')
    const sectionSonification = $('#sectionSonification')
    
    const inputFastaFile = $('#inputFastaFile')
    const inputBmp = $('#inputBmp')
    const inputScale = $('#inputScale')
    const inputsInstruments = $('input[id^=inputInstruments_]')
    const inputsStrategies = $('select[id^=inputsStrategies_]')

    const textMp3Filename = $('#textMp3Filename')
    const textMidiFilename = $('#textMidiFilename')
    const textJsonFilename = $('#textJsonFilename')
    
    const btnUploadFastaFile = $('#btnUploadFastaFile')
    const btnDownloadMp3File = $('#btnDownloadMp3File')
    const btnDownloadMidiFile = $('#btnDownloadMidiFile')
    const btnDownloadJsonFile = $('#btnDownloadJsonFile')
    const btnPlayMp3File = $('#btnPlayMp3File')
    const btnPlayMidiFile = $('#btnPlayMidiFile')
    const btnUpdateSonification = $('#btnUpdateSonification')

    btnUploadFastaFile.click((e) => {
        e.preventDefault()
        inputFastaFile.click()
    })

    inputFastaFile.change((e) => {
        let file = e.target.files[0]
        let spinner = btnUploadFastaFile.find('.spinner')

        if (!file) {
            inputFastaFile.click()
        }

        spinner.show()
        btnUploadFastaFile.attr('disabled', true)

        let data = new FormData
        data.append('file', file)

        requestSonificationData(data)
            .then((response) => {
                fillSonificationParameters(response)
                sectionStart.toggle()
                sectionSonification.toggle()
            }).catch((error) => {
                console.log(error)
                btnUploadFastaFile.attr('disabled', false)
            }).finally(() => {
                spinner.hide()
            })
    })

    btnPlayMp3File.click((e) => {
        e.preventDefault()
        alert('Play Mp3')
    })

    btnPlayMidiFile.click((e) => {
        e.preventDefault()
        alert('Play MIDI')
    })

    btnUpdateSonification.click((e) => {
        e.preventDefault()
        
        let file = inputFastaFile.prop('files')[0]
        let spinner = btnUpdateSonification.find('.spinner')

        if (!file) {
            inputFastaFile.click()
        }

        spinner.show()
        btnUpdateSonification.attr('disabled', true)

        let instruments = []
        
        inputsInstruments.each((i, input) => {
            instruments[i] = input.value
        })

        let strategies = []
        
        inputsStrategies.each((i, input) => {
            strategies[i] = input.value
        })

        let data = new FormData
        data.append('file', file)
        data.append('bmp', inputBmp.val())
        data.append('scale', inputScale.val())
        data.append('instruments', JSON.stringify(instruments))
        data.append('strategies', JSON.stringify(strategies))

        console.log(data)

        requestSonificationData(data)
            .then((response) => {
                fillSonificationParameters(response)
            }).catch((error) => {
                console.log(error)
            }).finally(() => {
                spinner.hide()
                btnUpdateSonification.attr('disabled', false)
            })
    })

    const requestSonificationData = async (data) => {
        return await $.ajax({
            url: 'http://localhost:8000',
            type: 'POST',
            data: data,
            cache: false,
            contentType: false,
            processData: false,
        })
    }

    const fillSonificationParameters = (data) => {
        inputBmp.val(data.bmp)
        inputScale.val(data.scale)

        textMp3Filename.text(data.mp3.filename)
        textMidiFilename.text(data.midi.filename)
        textJsonFilename.text(data.json.filename)

        btnDownloadMp3File.attr('href', data.mp3.url)
        btnDownloadMidiFile.attr('href', data.midi.url)
        btnDownloadJsonFile.attr('href', data.json.url)

        inputsInstruments.each((i) => {
            $(inputsInstruments[i]).val(data.frames[i][0].instrument)
        })

        inputsStrategies.each((i) => {
            $(inputsStrategies[i]).val(data.strategies[i])
        })
    }
})