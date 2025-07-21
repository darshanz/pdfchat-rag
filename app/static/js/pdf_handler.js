$(document).ready(function () {  
        // PDF 
        pdfjsLib.GlobalWorkerOptions.workerSrc = 'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.worker.min.js';
        const $viewer = $('#pdf-canvas'); 
        const url = $viewer.data('pdf');;
        const loadingTask = pdfjsLib.getDocument(url);

        loadingTask.promise.then(function (pdf) {
        for (let pageNum = 1; pageNum <= pdf.numPages; pageNum++) {
            pdf.getPage(pageNum).then(function (page) {
            const scale = 1.5;
            const viewport = page.getViewport({ scale: scale });

            const canvas = document.createElement('canvas');
            const context = canvas.getContext('2d');
            canvas.height = viewport.height;
            canvas.width = viewport.width;

            $viewer.append(canvas);

            page.render({
                canvasContext: context,
                viewport: viewport
            });
            });
        }
        }); 
         
    });