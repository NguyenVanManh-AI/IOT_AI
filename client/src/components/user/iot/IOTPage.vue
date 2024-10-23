<template>
    <div style="color: white;">
        <div id="big">
            <div class="p-2 m-2">
                <button type="button" class="btn btn-primary m-2" @click="toggleFan">
                    <i class="fa-solid" :class="isFanOn ? 'fa-xmark' : 'fa-check'"></i>
                    {{ isFanOn ? 'OFF FAN' : 'ON FAN' }}
                </button>
                <button type="button" class="btn btn-primary m-2" @click="toggleLed">
                    <i class="fa-solid" :class="isLedOn ? 'fa-xmark' : 'fa-check'"></i>
                    {{ isLedOn ? 'OFF LED' : 'ON LED' }}
                </button>
            </div>
            <audio style="display: none;" ref="audioPlayer" controls></audio>
        </div>
        <div>
            <div class="mic" :class="{ 'active-mic': isRecording }" style="color: white;" @click="toggleRecording">
                <span><i class="mic-icon"></i></span>
                <div v-if="isRecording" class="mic-shadow"></div>
            </div>
        </div>
    </div>
</template>

<script>
// import UserRequest from '@/restful/UserRequest';

export default {
    name: "IOTPage",
    props: {
    },
    setup() {

    },
    data() {
        return {
            mediaRecorder: null,
            audioChunks: [],
            isRecording: false,
            isFanOn: false,
            isLedOn: false,
            // selectedFile: null,
            // record: {
            //     id_folder: null,
            //     file: null,
            // },
            // errors: {
            //     id_folder: null,
            //     file: null,
            // }
        }
    },
    mounted() {
    },
    components: {
    },
    computed: {
    },
    methods: {
        async toggleRecording() {
            if (this.isRecording) {
                this.stopRecording();
            } else {
                await this.startRecording();
            }
        },
        async startRecording() {
            try {
                const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
                this.mediaRecorder = new MediaRecorder(stream);

                this.mediaRecorder.start();
                this.audioChunks = [];
                this.isRecording = true; // Đặt trạng thái ghi âm

                this.mediaRecorder.ondataavailable = (event) => {
                    this.audioChunks.push(event.data);
                };

                console.log("Recording started...");
            } catch (error) {
                console.error("Microphone access denied or not supported.", error);
            }
        },
        stopRecording() {
            if (this.mediaRecorder && this.mediaRecorder.state !== "inactive") {
                this.mediaRecorder.stop();

                this.mediaRecorder.onstop = () => {
                    const audioBlob = new Blob(this.audioChunks, { type: "audio/wav" });
                    const audioUrl = URL.createObjectURL(audioBlob);
                    this.$refs.audioPlayer.src = audioUrl;
                    this.uploadAudio(audioBlob);
                    this.isRecording = false; // Đặt trạng thái ghi âm về false
                    console.log("Recording stopped.");
                };
            }
        },
        async uploadAudio(audioBlob) {
            const formData = new FormData();
            formData.append("audio", audioBlob, "recording.wav");

            try {
                const response = await fetch("http://localhost:8000/api/upload-audio/", {
                    method: "POST",
                    body: formData,
                });

                if (response.ok) {
                    console.log("Audio uploaded successfully.");
                } else {
                    console.error("Error uploading audio:", response.status);
                }
            } catch (error) {
                console.error("Failed to upload audio:", error);
            }
        },
        async sendMotorCommand(option) {
            const url = "http://192.168.162.168/sendOption"; // Địa chỉ IP của ESP8266
            const data = new URLSearchParams();
            data.append("option", option);

            try {
                const response = await fetch(url, {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/x-www-form-urlencoded",
                    },
                    body: data.toString(),
                });

                if (response.ok) {
                    console.log("Gửi thành công, Động cơ đã được điều khiển theo tùy chọn:", option);
                } else {
                    console.error("Có lỗi xảy ra khi gửi yêu cầu:", response.status);
                }
            } catch (error) {
                console.error("Không thể kết nối đến ESP8266:", error);
            }
        },
        toggleFan() {
            this.isFanOn = !this.isFanOn;
            this.sendMotorCommand(this.isFanOn ? 1 : 2); // 1: Bật FAN, 2: Tắt FAN
        },
        toggleLed() {
            this.isLedOn = !this.isLedOn;
            this.sendMotorCommand(this.isLedOn ? 3 : 4); // 3: Bật LED, 4: Tắt LED
        }
    },
    watch: {

    },
}
</script>
<style scoped>
/* image upload */
.big-container-image {
    display: flex;
    align-items: center;
    align-content: center;
    /* height: 100%; */
}

.inner-image-upload {
    height: 50%;
    width: 100%;
}

.min-image-upload {
    background-color: #e9ecef;
    position: relative;
    text-align: center;
    /* width: 170px; */
    height: 170px;
    border-radius: 6px;
    cursor: pointer;
    display: flex;
    justify-content: center;
    align-items: center;
    transition: all 0.5s ease;
    width: 100%;
}

.min-image-upload .preview {
    /* width: 150px; */
    height: 150px;
    object-fit: cover;
    border-radius: 6px;
    cursor: default;
    width: 100%;
}

.min-image-upload:hover {
    transition: all 0.5s ease;
    background: #E8F5E9;
}

.input-file {
    opacity: 0;
    top: 0px;
    left: 0px;
    position: absolute;
    cursor: pointer;
    /* width: 150px; */
    height: 150px;
    width: 100%;
}

.box-preview {
    position: relative;
}

.iconClound {
    cursor: pointer;
    font-size: 60px;
    color: var(--user-color);
}

.close-img {
    position: absolute;
    top: -6px;
    right: -6px;
    width: 16px;
}

/* image upload */


/*  */
.modal-dialog {
    max-width: 800px;
}

/*  */


.modal.fade.show {
    padding-left: 0px;
}

.modal-content {
    /* margin-top: 100px; */
    border-radius: 10px;
}

.bigContainer .input-form {
    height: 40px;
    width: 100%;
    position: relative;
}

.bigContainer .input-form input {
    height: 100%;
    width: 100%;
    border: none;
    font-size: 17px;
    border-bottom: 2px solid silver;
    outline: none !important;
}

.input-form input:focus~label,
.input-form input:valid~label {
    transform: translateY(-20px);
    font-size: 15px;
    color: var(--user-color);
}

.input-form .underline.fix2:before {
    position: absolute;
    content: "";
    height: 100%;
    width: 100%;
    background: var(--user-color);
    transform: scaleX(0);
    transform-origin: center;
    transition: transform 0.3s ease;
}

.bigContainer .input-form label {
    position: absolute;
    bottom: 0px;
    left: 0;
    color: grey;
    pointer-events: none;
    transition: all 0.3s ease;
}

.input-form .underline {
    position: absolute;
    height: 2px;
    width: 100%;
    bottom: 0;
}

.input-form .underline:before {
    position: absolute;
    content: "";
    height: 100%;
    width: 100%;
    background: var(--user-color);
    transform: scaleX(0);
    transform-origin: center;
    transition: transform 0.3s ease;
}

.input-form input:focus~.underline:before,
.input-form input:valid~.underline:before {
    transform: scaleX(1);
}

@import url('https://fonts.googleapis.com/css2?family=Reem+Kufi+Ink');

#big {
    display: flex;
    position: relative;
}

.btn-pers {
    position: relative;
    left: 50%;
    padding: 1em 2.5em;
    font-size: 12px;
    text-transform: uppercase;
    letter-spacing: 2.5px;
    font-weight: 700;
    color: #000;
    background-color: #fff;
    border: none;
    border-radius: 45px;
    box-shadow: 0px 8px 15px rgba(0, 0, 0, 0.1);
    transition: all 0.3s ease 0s;
    cursor: pointer;
    outline: none;
    transform: translateX(-50%);
}

.btn-pers:hover {
    background-color: var(--user-color);
    box-shadow: var(--btn-hover);
    color: #fff;
    transform: translate(-50%, -7px);
}

.btn-pers:active {
    transform: translate(-50%, -1px);
}

#inputPassword {
    padding-right: 26px;
}
</style>
<style src="./voice.css"></style>
