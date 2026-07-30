---
layout: page
title: Contact
permalink: /contact/
---

<!-- TODO: vervang telefoonnummer, WhatsApp-nummer en Messenger-link door de echte gegevens -->

<div class="contact-reveal" id="contact-reveal">
  <p class="lead contact-intro reveal-line reveal-line--1">Interesse in een shoot of reportage? Neem rechtstreeks contact op — ik reageer snel.</p>

  <div class="contact-list">
    <a class="contact-row reveal-line reveal-line--2" href="mailto:info@jelcofotografie.be">
      <span class="contact-row-label data-strip">E-mail</span>
      <span class="contact-row-value">info@jelcofotografie.be</span>
      <span class="contact-row-arrow"><svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.6"><path class="contact-row-arm contact-row-arm-top" d="M6 4L10 8"/><path class="contact-row-arm contact-row-arm-bot" d="M10 8L6 12"/></svg></span>
    </a>
    <a class="contact-row reveal-line reveal-line--3" href="tel:+32000000000">
      <span class="contact-row-label data-strip">Telefoon</span>
      <span class="contact-row-value">+32 000 00 00 00</span>
      <span class="contact-row-arrow"><svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.6"><path class="contact-row-arm contact-row-arm-top" d="M6 4L10 8"/><path class="contact-row-arm contact-row-arm-bot" d="M10 8L6 12"/></svg></span>
    </a>
    <a class="contact-row reveal-line reveal-line--4" href="https://wa.me/32000000000" target="_blank" rel="noopener">
      <span class="contact-row-label data-strip">WhatsApp</span>
      <span class="contact-row-value">Stuur een bericht</span>
      <span class="contact-row-arrow"><svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.6"><path class="contact-row-arm contact-row-arm-top" d="M6 4L10 8"/><path class="contact-row-arm contact-row-arm-bot" d="M10 8L6 12"/></svg></span>
    </a>
    <a class="contact-row reveal-line reveal-line--5" href="https://m.me/jelcofotografie" target="_blank" rel="noopener">
      <span class="contact-row-label data-strip">Messenger</span>
      <span class="contact-row-value">Stuur een bericht</span>
      <span class="contact-row-arrow"><svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.6"><path class="contact-row-arm contact-row-arm-top" d="M6 4L10 8"/><path class="contact-row-arm contact-row-arm-bot" d="M10 8L6 12"/></svg></span>
    </a>
    <a class="contact-row reveal-line reveal-line--6" href="https://instagram.com/jelcofotografie" target="_blank" rel="noopener">
      <span class="contact-row-label data-strip">Instagram</span>
      <span class="contact-row-value">@jelcofotografie</span>
      <span class="contact-row-arrow"><svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.6"><path class="contact-row-arm contact-row-arm-top" d="M6 4L10 8"/><path class="contact-row-arm contact-row-arm-bot" d="M10 8L6 12"/></svg></span>
    </a>
  </div>
</div>

<script>
  (function () {
    var reveal = document.getElementById('contact-reveal');
    if (!reveal) return;
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
      reveal.classList.add('is-revealed');
      return;
    }
    requestAnimationFrame(function () {
      requestAnimationFrame(function () {
        reveal.classList.add('is-revealed');
      });
    });
  })();
</script>
