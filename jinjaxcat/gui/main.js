window.formLogic = {
    inputFiles: [],
    template: null,
    outputFile: null,
    validationType: null,
    xmlValidationFile: null,
    prettifyOutput: true,
    isLoading: false,
    activePreset: null,
    allPresetNames: [],
    log: '',
    showModal: false,
    modalMsg: '',

    async chooseTemplate() {
        this.isLoading = true;
        const result = await eel.choose_template();
        this.template = await result();
        updateLog(`New template file loaded: ${this.template}`);
        this.isLoading = false;
    },

    async chooseInputFiles() {
        this.isLoading = true;
        const resultFunc = await eel.choose_input_files(this.inputFiles);
        const files = await resultFunc();
        if (files) {
            this.inputFiles = files;
        }
        updateLog(`New input files loaded: ${JSON.stringify(this.inputFiles)}`);
        this.isLoading = false;
    },

    async chooseValidationFile() {
        this.isLoading = true;
        const resultFunc = await eel.choose_xml_validation_file();
        this.xmlValidationFile = await resultFunc();
        updateLog(`New validation file chosen: ${this.xmlValidationFile}`);
        this.isLoading = false;
    },

    removeFile(index) {
        this.inputFiles.splice(index, 1);
        updateLog(`Input file removed.`);
    },

    resetPresetSelection() {
        console.log(this.$refs.presetSelect.value);
        this.$refs.presetSelect.value = 'Select Preset';
        this.activePreset = null;
    },

    validateForm() {
        if (this.inputFiles.length === 0) {
            updateLog('Please select input files!', true);
            return false;
        }
        if (this.xmlValidation && !this.xmlValidationFile) {
            updateLog('Please select an XML validation file!', true);
            return false;
        }
        if (!(this.inputFiles.length > 0 && this.template)) {
            updateLog('Please fill all required fields!', true);
            return false;
        }
        return true;
    },

    async submitForm() {
        this.isLoading = true;
        if (!this.validateForm()) {
            this.isLoading = false;
            return;
        }
        const result = await eel.choose_output_file();
        this.outputFile = await result();
        if (!this.outputFile) {
            updateLog("No output file selected!", true);
            this.isLoading = false;
            return;
        }
        const isDone = await eel.execute_rendering_workflow(
            this.inputFiles,
            this.template,
            this.outputFile,
            this.prettifyOutput,
            this.validationType,
            this.xmlValidationFile
        );
        const generationStatus = await isDone();
        if (generationStatus) {
            updateLog("The catalog has been generated.", true);
        } else {
            updateLog("Error during catalog generation.");
        }
        this.isLoading = false;
    },

    async savePreset() {
        if (!this.validateForm()) {
            return;
        }
        let presetName = prompt("Enter preset name:");
        if (!presetName || presetName === "") {
            updateLog("You must enter a name for the preset!", true);
            return;
        }
        if (this.allPresetNames.includes(presetName)) {
            updateLog("Preset name already exists. Please choose a different name!", true);
            return;
        }
        await eel.save_preset(presetName, [
            this.inputFiles,
            this.template,
            this.outputFile,
            this.prettifyOutput,
            this.validationType,
            this.xmlValidationFile
        ]);
        await this.refreshPresetNames();
        this.$refs.presetSelect.value = presetName;
        this.activePreset = presetName;
    },

    async loadPreset(presetName) {
        const resultFunc = await eel.get_preset_data(presetName);
        [
            this.inputFiles,
            this.template,
            this.outputFile,
            this.prettifyOutput,
            this.validationType,
            this.xmlValidationFile
        ] = await resultFunc();
        this.activePreset = presetName;
    },

    async refreshPresetNames() {
        const resultFunc = await eel.get_preset_names();
        this.allPresetNames = await resultFunc();
        this.resetPresetSelection();
    }
};

eel.expose(updateLog);

function updateLog(msg, isAlert = false) {
    const now = new Date();
    now.setMinutes(now.getMinutes() - now.getTimezoneOffset());
    const timestamp = now.toISOString().slice(0, 16).replace('T', ' ');
    window.x_data.log += `${timestamp} | ${msg}\n`;
    if (isAlert) {
        window.x_data.showModal = true
        window.x_data.modalMsg = msg
    }
}