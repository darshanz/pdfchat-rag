$(document).ready(function () {
        $('#chat-spinner').css('display', 'none');
        $('#chat_progressbar').css('display', 'none');
        $('#send-btn').css('display', 'inline-block');
        $('#chat-input').removeAttr('disabled');

        // Chat 
        function appendMessage(text, isUser = false) {
        const $div = $('<div>')
            .addClass('chat-bubble' + (isUser ? ' user' : ''))
            .html(text);
        $('#chat-messages').append($div);
        $('#chat-messages').scrollTop($('#chat-messages')[0].scrollHeight);
        }

        function sendMessage() {
            $('#send-btn').css('display', 'none');
            $('#chat-spinner').css('display', 'inline-block');
            $('#chat_progressbar').css('display', 'inline-block');
            $('#chat-input').attr('disabled', true);



        const text = $('#chat-input').val().trim();
        if (!text) return;

        appendMessage(text, true); // show user message
        $('#chat-input').val('');

        $.ajax({
            type: 'POST',
            url: '/send-chat',
            contentType: 'application/json',
            data: JSON.stringify({
            query: text,
            paper_id: $('#chat-input').data('paperid')
            }),
            success: function (response) {
            console.log('Response from /send-chat:', response);
                
            },
            error: function (xhr, status, error) {
            console.error('Error from /send-chat:', error);
            appendMessage('Sorry! There is some problem with the system. Please check later.', false);
            
            }
        });
        }

        $('#send-btn').on('click', sendMessage);
        $('#chat-input').on('keydown', function (e) {
        if (e.key === 'Enter') sendMessage();
        }); 

        const socket = io({ transports: ['polling', 'websocket'], debug: true });

        socket.on('connect', function () {
        console.log('Successfully connected to the server via WebSocket');
        });

        socket.on('chat_response', function (data) {
            console.log('Chat response received:', data);
            appendMessage(data.message);
            $('#chat-spinner').css('display', 'none');
            $('#chat_progressbar').css('display', 'none'); 
            $('#send-btn').css('display', 'inline-block');
            $('#chat-input').removeAttr('disabled');
            
        });
    });