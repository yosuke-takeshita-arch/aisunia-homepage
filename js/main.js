'use strict';

/* ========================================
   Header: scroll shadow
   ======================================== */
const header = document.getElementById('header');

const onScroll = () => {
  header.classList.toggle('scrolled', window.scrollY > 10);
};

window.addEventListener('scroll', onScroll, { passive: true });

/* ========================================
   Mobile menu
   ======================================== */
const menuBtn = document.querySelector('.header__menu-btn');
const nav     = document.querySelector('.header__nav');

menuBtn.addEventListener('click', () => {
  const isOpen = nav.classList.toggle('is-open');
  menuBtn.classList.toggle('is-active', isOpen);
  menuBtn.setAttribute('aria-expanded', String(isOpen));
  document.body.style.overflow = isOpen ? 'hidden' : '';
});

// Close menu on nav link click
nav.querySelectorAll('a').forEach(link => {
  link.addEventListener('click', () => {
    nav.classList.remove('is-open');
    menuBtn.classList.remove('is-active');
    menuBtn.setAttribute('aria-expanded', 'false');
    document.body.style.overflow = '';
  });
});

/* ========================================
   Scroll animations (IntersectionObserver)
   ======================================== */
const animTargets = document.querySelectorAll('.fade-in, .fade-up');

const observer = new IntersectionObserver(
  (entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('is-visible');
        observer.unobserve(entry.target);
      }
    });
  },
  { threshold: 0.12 }
);

animTargets.forEach(el => observer.observe(el));

/* ========================================
   Contact form: client-side validation + Formspree送信
   ======================================== */
const FORMSPREE_ENDPOINT = 'https://formspree.io/f/mvzveqaz';

const form = document.getElementById('contactForm');

form.addEventListener('submit', (e) => {
  e.preventDefault();

  const fields = [
    { id: 'name',    label: 'お名前' },
    { id: 'email',   label: 'メールアドレス' },
    { id: 'message', label: 'お問い合わせ内容' },
  ];

  clearErrors();

  const errors = fields.reduce((acc, { id, label }) => {
    const el = document.getElementById(id);
    if (!el.value.trim()) {
      acc.push({ el, msg: `${label}を入力してください。` });
    } else if (id === 'email' && !isValidEmail(el.value)) {
      acc.push({ el, msg: '正しいメールアドレスを入力してください。' });
    }
    return acc;
  }, []);

  if (errors.length > 0) {
    errors.forEach(({ el, msg }) => showError(el, msg));
    errors[0].el.focus();
    return;
  }

  const submitBtn = form.querySelector('[type="submit"]');
  submitBtn.disabled = true;
  submitBtn.textContent = '送信中...';

  fetch(FORMSPREE_ENDPOINT, {
    method: 'POST',
    headers: { 'Accept': 'application/json' },
    body: new FormData(form),
  })
    .then((res) => {
      if (res.ok) {
        showSuccess();
      } else {
        submitBtn.disabled = false;
        submitBtn.textContent = '送信する';
        showSendError();
      }
    })
    .catch(() => {
      submitBtn.disabled = false;
      submitBtn.textContent = '送信する';
      showSendError();
    });
});

function isValidEmail(value) {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value);
}

function showError(input, message) {
  input.classList.add('is-error');
  input.setAttribute('aria-invalid', 'true');

  const errEl = document.createElement('p');
  errEl.className = 'form-error';
  errEl.textContent = message;
  errEl.style.cssText = 'color:#BC002D;font-size:0.8rem;margin-top:4px;';
  input.insertAdjacentElement('afterend', errEl);
}

function clearErrors() {
  form.querySelectorAll('.is-error').forEach(el => {
    el.classList.remove('is-error');
    el.removeAttribute('aria-invalid');
  });
  form.querySelectorAll('.form-error').forEach(el => el.remove());
}

function showSuccess() {
  form.innerHTML = `
    <div style="text-align:center;padding:48px 0;">
      <p style="font-size:2rem;margin-bottom:16px;">&#10003;</p>
      <p style="font-size:1.1rem;font-weight:700;color:#1A2B4A;margin-bottom:8px;">
        お問い合わせを受け付けました
      </p>
      <p style="font-size:0.875rem;color:#555;">
        通常2営業日以内にご返信いたします。
      </p>
    </div>
  `;
}

function showSendError() {
  const errEl = document.createElement('p');
  errEl.textContent = '送信に失敗しました。時間をおいて再度お試しください。';
  errEl.style.cssText = 'color:#BC002D;font-size:0.875rem;text-align:center;margin-top:16px;';
  form.appendChild(errEl);
}
