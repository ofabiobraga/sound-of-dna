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

    const playerMidi = $('#playerMidi')

    let frames = []
    let toPlayFrames = []
    let toPlayNotes = []

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

        spinner.show('fast')
        btnUploadFastaFile.attr('disabled', true)

        let data = new FormData
        data.append('file', file)

        requestSonificationData(data)
            .then((response) => {
                fillSonificationParameters(response)
                sectionStart.slideToggle(1000)
                sectionSonification.show(500)
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

    const configurePlayerMidi = () => {
        const __pitchToNoteName = (pitch) => {
            const noteNames = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B'];
            const noteIndex = (pitch + 9) % 12;
            const octave = Math.floor((pitch + 9) / 12) - 1;

            return `${noteNames[noteIndex]}${octave}`;
        }

        playerMidi[0].addEventListener('load', (event) => {
            toPlayNotes = $('#playerMidi')[0].ns.notes

            toPlayFrames[0] = toPlayNotes.filter((note) => note.instrument == 0)
            toPlayFrames[1] = toPlayNotes.filter((note) => note.instrument == 1)
            toPlayFrames[2] = toPlayNotes.filter((note) => note.instrument == 2)
            toPlayFrames[3] = toPlayNotes.filter((note) => note.instrument == 3)
        })

        playerMidi[0].addEventListener('note', (event) => {
            let playedNote = event.detail.note
            let playedFrame = playedNote.instrument
            let otherFrames = [0, 1, 2, 3].filter((frame) => frame != playedFrame)
            let playedCodon = frames[playedFrame][toPlayFrames[playedFrame].indexOf(playedNote)]
            let frameColorMapping = ['warning', 'success', 'danger', 'primary']
            let element = $(document.createElement('button'))
                .addClass('col-md-2 btn btn-sm btn-' + frameColorMapping[playedFrame])
                .html(playedCodon.value + ' <span class="badge text-bg-light">' + __pitchToNoteName(playedNote.pitch) + '</span>')
                .hide()

            $('#liInstrument_' + playedFrame).append(element)
            
            element.fadeIn('fast')

            if ($('#liInstrument_' + playedFrame).children().length > 5) {
                $('#liInstrument_' + playedFrame).children().first().remove()
            }

            otherFrames.forEach((otherFrame) => {
                let element = $(document.createElement('button'))
                    .addClass('col-md-2 btn btn-sm btn-light')
                    .html('.')

                if ($('#liInstrument_' + otherFrame).children().length > 5) {
                    $('#liInstrument_' + otherFrame).children().first().remove()
                }
                
                $('#liInstrument_' + otherFrame).append(element)
            })
        })
    }

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

        playerMidi.attr('src', data.midi.url)

        frames = data.frames
    }

    configurePlayerMidi()
})