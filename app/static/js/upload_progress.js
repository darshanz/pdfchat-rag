$(document).ready(function() {
    const socket = io({ transports: ['polling', 'websocket'], debug: true });
    socket.on('connect', function() {
        console.log('Successfully connected to the server via WebSocket');
    });
      socket.on('task_progress', function(data) {
          console.log('Progress update received:', data);
          $('#progress-bar').attr('value', data.progress);
          if (data.progress == 100) {
              window.location.href = $('#progress-bar').data('redirecturl');  
          }
        });
    });