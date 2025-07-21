$(document).ready(function () {
    const $dropZone = $('#drop-zone');
    const $fileInput = $('#file-input');
    const $fileLabel = $('#file-label');
    const $btnUploadPaper = $('#btnUploadPaper');
    const $formUploadPaper = $('#formUploadPaper');

    let selectedFile = null;

    // Drag events
    $dropZone.on('dragover', function (e) {
        e.preventDefault();
        $dropZone.addClass('dragover');
    });

    $dropZone.on('dragleave', function () {
        $dropZone.removeClass('dragover');
    });

    $dropZone.on('click', function () {
        $fileInput[0].click();
    });

    $dropZone.on('drop', function (e) {
        e.preventDefault();
        $dropZone.removeClass('dragover');

        const files = e.originalEvent.dataTransfer.files;
        if (files.length && files[0].type === 'application/pdf') {
            selectedFile = files[0];
            handleFile(selectedFile);
        } else {
            $fileLabel.text("Please drop a valid PDF file.");
        }
    });

    // File input change
    $fileInput.on('change', function () {
        const file = this.files[0];
        if (file && file.type === 'application/pdf') {
            selectedFile = file;
            handleFile(selectedFile);
        } else {
            $fileLabel.text("Please select a valid PDF file.");
        }
    });

    function handleFile(file) {
        $fileLabel.text(`Selected: ${file.name}`);
        console.log("PDF File ready:", file);
    }

    // Upload via AJAX using form's action URL
    $btnUploadPaper.on('click', function (event) {
        event.preventDefault();

        if (!selectedFile || selectedFile.type !== 'application/pdf') {
            $fileLabel.text("Please select a valid PDF file.");
            return;
        }

        const formData = new FormData();
        formData.append('file', selectedFile);

        const uploadUrl = $formUploadPaper.attr('action');

        $.ajax({
            url: uploadUrl,
            type: 'POST',
            data: formData,
            processData: false,
            contentType: false,
            success: function (response) {
                console.log("Upload successful", response);
                $fileLabel.text("Upload successful.");
                window.location.href = '/processing/' + response.paper_id;
            },
            error: function (err) {
                console.error("Upload failed", err);
                $fileLabel.text("Upload failed. Try again.");
            }
        });
    });
});
