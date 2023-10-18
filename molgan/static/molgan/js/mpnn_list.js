const fileUpload = document.getElementById("customFileLg");
const fileName = document.getElementById("file-name");

fileUpload.addEventListener("change", function (event) {
const file = this.files[0];
if (file) {
    fileName.textContent = file.name;
} else {
    fileName.textContent = "Choose a file";
}
});