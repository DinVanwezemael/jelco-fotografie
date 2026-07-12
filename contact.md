---
layout: page
title: Contact
permalink: /contact/
---

<!-- TODO: vervang telefoonnummer, WhatsApp-nummer en Messenger-link door de echte gegevens -->

<div class="contact-grid">
  <form class="contact-form" id="contact-form">
    <p class="lead">Interesse in een shoot of reportage? Stuur een bericht.</p>

    <div class="field">
      <label for="cf-name">Naam</label>
      <input type="text" id="cf-name" name="name" required>
    </div>

    <div class="field">
      <label for="cf-email">E-mail</label>
      <input type="email" id="cf-email" name="email" required>
    </div>

    <div class="field">
      <label for="cf-message">Bericht</label>
      <textarea id="cf-message" name="message" rows="6" required></textarea>
    </div>

    <button type="submit" class="button">Verstuur bericht</button>
  </form>

  <aside class="contact-info">
    <div class="direct-contact">
      <p><span>E-mail</span><strong><a href="mailto:info@jelcofotografie.be">info@jelcofotografie.be</a></strong></p>
      <p><span>Telefoon</span><strong><a href="tel:+32000000000">+32 000 00 00 00</a></strong></p>
    </div>

    <div class="social-buttons">
      <a class="social-button" href="https://wa.me/32000000000" target="_blank" rel="noopener">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><path d="M4 20l1.3-3.8A7.6 7.6 0 1 1 8.6 19L4 20Z"/><path d="M8.5 9.3c0 3.6 2.9 6.3 6.4 6.3.5 0 1-.4 1-1v-1.1a.7.7 0 0 0-.5-.6l-1.8-.6a.7.7 0 0 0-.8.3l-.3.5a5 5 0 0 1-2.5-2.5l.5-.3a.7.7 0 0 0 .3-.8l-.6-1.8a.7.7 0 0 0-.6-.5H8.9c-.5 0-.4.5-.4 1Z"/></svg>
        <span>WhatsApp</span>
      </a>
      <a class="social-button" href="https://m.me/jelcofotografie" target="_blank" rel="noopener">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><path d="M12 4C6.9 4 3 7.6 3 12.2c0 2.5 1.2 4.7 3.1 6.2v2.9l2.9-1.6c1 .3 2 .4 3 .4 5.1 0 9-3.6 9-8.2S17.1 4 12 4Z"/><path d="M7.5 13.4 11 10l2.4 2 3.6-3.4-4 4.4-2.3-2-3.7 3.6Z" fill="currentColor" stroke="none"/></svg>
        <span>Messenger</span>
      </a>
      <a class="social-button" href="https://instagram.com/jelcofotografie" target="_blank" rel="noopener">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><rect x="3.5" y="3.5" width="17" height="17" rx="4"/><circle cx="12" cy="12" r="4"/><circle cx="17" cy="7" r="1" fill="currentColor" stroke="none"/></svg>
        <span>Instagram</span>
      </a>
    </div>
  </aside>
</div>

<script>
  document.getElementById('contact-form').addEventListener('submit', function (e) {
    e.preventDefault();
    var name = document.getElementById('cf-name').value;
    var email = document.getElementById('cf-email').value;
    var message = document.getElementById('cf-message').value;
    var subject = encodeURIComponent('Contactaanvraag via website — ' + name);
    var body = encodeURIComponent('Naam: ' + name + '\nE-mail: ' + email + '\n\n' + message);
    window.location.href = 'mailto:info@jelcofotografie.be?subject=' + subject + '&body=' + body;
  });
</script>
