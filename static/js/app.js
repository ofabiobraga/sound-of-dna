$(document).ready(() => {
    const sectionStart = $('#sectionStart')
    const sectionSonification = $('#sectionSonification')
    
    const inputFastaFile = $('#inputFastaFile')
    const inputBmp = $('#inputBmp')
    const inputScale = $('#inputScale')
    const inputsInstruments = $('select[id^=inputInstruments_]')
    const inputsStrategies = $('select[id^=inputsStrategies_]')
    const inputsInitialOctaves = $('input[id^=inputInitialOctaves_]')

    const textMp3Filename = $('#textMp3Filename')
    const textMidiFilename = $('#textMidiFilename')
    const textJsonFilename = $('#textJsonFilename')
    const textBioDescription = $('#textBioDescription')
    const textBioNucletides = $('#textBioNucletides')
    const textBioGCATRatio = $('#textBioGCATRatio')
    
    const btnUploadFastaFile = $('#btnUploadFastaFile')
    const btnDownloadMp3File = $('#btnDownloadMp3File')
    const btnDownloadMidiFile = $('#btnDownloadMidiFile')
    const btnDownloadJsonFile = $('#btnDownloadJsonFile')
    const btnPlayMp3File = $('#btnPlayMp3File')
    const btnPlayMidiFile = $('#btnPlayMidiFile')
    const btnUpdateSonification = $('#btnUpdateSonification')

    const playerMidi = $('#playerMidi')

    const midiIntrumentCodes = {
        "Piano": {
            0: "Acoustic Grand Piano",
            1: "Bright Acoustic Piano",
            2: "Electric Grand Piano",
            3: "Honky-tonk Piano",
            4: "Rhodes Piano",
            5: "Chorused Piano",
            6: "Harpsichord",
            7: "Clavinet"
        },
        "Chormatic Percussion": {
            8: "Celesta",
            9: "Glockenspiel",
            10: "Music Box",
            11: "Vibraphone",
            12: "Marimba",
            13: "Xylophone",
            14: "Tubular Bells",
            15: "Dulcimer",
        },
        "Organ Timbres": {
            16: "Hammond Organ",
            17: "Percussive Organ",
            18: "Rock Organ",
            19: "Church Organ",
            20: "Reed Organ",
            21: "Accordion",
            22: "Harmonica",
            23: "Tango Accordion",
        },
        "Guitar Timbres": {
            24: "Acoustic Nylon Guitar",
            25: "Acoustic Steel Guitar",
            26: "Electric Jazz Guitar",
            27: "Electric Clean Guitar",
            28: "Electric Muted Guitar",
            29: "Overdriven Guitar",
            30: "Distortion Guitar",
            31: "Guitar Harmonics",
        },
        "Bass Timbres": {
            32: "Acoustic Bass",
            33: "Fingered Electric Bass",
            34: "Plucked Electric Bass",
            35: "Fretless Bass",
            36: "Slap Bass 1",
            37: "Slap Bass 2",
            38: "Synth Bass 1",
            39: "Synth Bass 2",
        },
        "String Timbres": {
            40: "Violin",
            41: "Viola",
            42: "Cello",
            43: "Contrabass",
            44: "Tremolo Strings",
            45: "Pizzicato Strings",
            46: "Orchestral Harp",
            47: "Timpani",
        },
        "Ensemble Timbres": {
            48: "String Ensemble 1",
            49: "String Ensemble 2",
            50: "Synth Strings 1",
            51: "Synth Strings 2",
            52: "Choir Aah",
            53: "Choir Ooh",
            54: "Synth Voice",
            55: "Orchestral Hit",
        },
        "Brass Timbres": {
            56: "Trumpet",
            57: "Trombone",
            58: "Tuba",
            59: "Muted Trumpet",
            60: "French Horn",
            61: "Brass Section",
            62: "Synth Brass 1",
            63: "Synth Brass 2",
        },
        "Reed Timbres": {
            64: "Soprano Sax",
            65: "Alto Sax",
            66: "Tenor Sax",
            67: "Baritone Sax",
            68: "Oboe",
            69: "English Horn",
            70: "Bassoon",
            71: "Clarinet",
        },
        "Pipe Timbres": {
            72:	"Piccolo",
            73:	"Flute",
            74:	"Recorder",
            75:	"Pan Flute",
            76:	"Bottle Blow",
            77:	"Shakuhachi",
            78:	"Whistle",
            79:	"Ocarina",
        },
        "Synth Lead": {
            80:	"Square Wave Lead",
            81:	"Sawtooth Wave Lead",
            82:	"Calliope Lead",
            83:	"Chiff Lead",
            84:	"Charang Lead",
            85:	"Voice Lead",
            86:	"Fifths Lead",
            87:	"Bass Lead",
        },
        "Synth Pad": {
            88:	"New Age Pad",
            89:	"Warm Pad",
            90:	"Polysynth Pad",
            91:	"Choir Pad",
            92:	"Bowed Pad",
            93:	"Metallic Pad",
            94:	"Halo Pad",
            95:	"Sweep Pad",
        },
        "Synth Effects": {
            96: "Rain Effect",
            97: "Soundtrack Effect",
            98: "Crystal Effect",
            99: "Atmosphere Effect",
            100: "Brightness Effect",
            101: "Goblins Effect",
            102: "Echoes Effect",
            103: "Sci - Fi Effect",
        },
        "Ethnic Timbres": {
            104: "Sitar",
            105: "Banjo",
            106: "Shamisen",
            107: "Koto",
            108: "Kalimba",
            109: "Bagpipe",
            110: "Fiddle",
            111: "Shanai",
        },
        "Sound Effects": {
            112: "Tinkle Bell",
            113: "Agogo",
            114: "Steel Drums",
            115: "Woodblock",
            116: "Taiko Drum",
            117: "Melodic Tom",
            118: "Synth Drum",
            119: "Reverse Cymbal",
            120: "Guitar Fret Noise",
            121: "Breath Noise",
            122: "Seashore",
            123: "Bird Tweet",
            124: "Telephone Ring",
            125: "Helicopter",
            126: "Applause",
            127: "Gun Shot",
        },
    }

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

        let initialOctaves = []

        inputsInitialOctaves.each((i, input) => {
            initialOctaves[i] = input.value
        })

        let data = new FormData
        data.append('file', file)
        data.append('bmp', inputBmp.val())
        data.append('scale', inputScale.val())
        data.append('instruments', JSON.stringify(instruments))
        data.append('strategies', JSON.stringify(strategies))
        data.append('initial_octaves', JSON.stringify(initialOctaves))

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

    const buildSelectInstruments = () => {
        inputsInstruments.each((index, element) => {
            for (instrumentGroup in midiIntrumentCodes) {
                let optionGroup = $(document.createElement('optgroup'))
                    .attr('label', instrumentGroup)

                for (instrumentCode in midiIntrumentCodes[instrumentGroup]) {
                    let option = $(document.createElement('option'))
                        .attr('value', instrumentCode)
                        .text(midiIntrumentCodes[instrumentGroup][instrumentCode])

                    optionGroup.append(option)
                }

                $(element).append(optionGroup)
            }

            

            
        })
    }

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
        textBioDescription.text(data.description)
        textBioNucletides.text(data.frequencies['G'] + 'G, ' + data.frequencies['A'] + 'A, ' + data.frequencies['T'] + 'T, and ' + data.frequencies['C'] + 'C')
        textBioGCATRatio.text(data['gc/at'])

        btnDownloadMp3File.attr('href', data.mp3.url)
        btnDownloadMidiFile.attr('href', data.midi.url)
        btnDownloadJsonFile.attr('href', data.json.url)

        inputsInstruments.each((i) => {
            $(inputsInstruments[i]).val(data.frames[i][0].instrument)
        })

        inputsStrategies.each((i) => {
            $(inputsStrategies[i]).val(data.strategies[i])
        })

        inputsInitialOctaves.each((i) => {
            $(inputsInitialOctaves[i]).val(data.initial_octaves[i])
        })

        playerMidi.attr('src', data.midi.url)

        frames = data.frames
    }

    buildSelectInstruments()
    configurePlayerMidi()
})