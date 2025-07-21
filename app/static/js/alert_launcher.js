const $container = $('.alert-toast-wrapper');
const $button = $container.find('sl-button');
let count = 0;

function escapeHtml(html) {
  return $('<div>').text(html).html();
}

function notify(message, variant = 'primary', icon = 'info-circle', duration = 3000) {
  const $alert = $('<sl-alert>', {
    variant: variant,
    closable: true,
    duration: duration,
    html: `
      <sl-icon name="${icon}" slot="icon"></sl-icon>
      ${escapeHtml(message)}
    `
  });

  $('body').append($alert);
  return $alert[0].toast();
}
