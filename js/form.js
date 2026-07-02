/* =========================================================
   ACTIVE GLOBAL IMPEX — form.js
   Vanilla re-implementation of src/hooks/useInquiryForm.ts (Zod schema)
   and src/lib/emailjs.ts (EmailJS send helper).

   >>> CONFIG REQUIRED BEFORE GOING LIVE <<<
   These three values are placeholders in the original project too
   (see .env.example: NEXT_PUBLIC_EMAILJS_SERVICE_ID / TEMPLATE_ID / PUBLIC_KEY).
   Replace them with real EmailJS credentials from https://www.emailjs.com/
   Template variables expected (must match the EmailJS template exactly):
     {{from_name}} {{from_email}} {{phone}} {{company}} {{country}}
     {{product}} {{quantity}} {{message}} {{to_email}}
   ========================================================= */

(function () {
  "use strict";

  var EMAILJS_SERVICE_ID = "service_xxxxxxx";
  var EMAILJS_TEMPLATE_ID = "template_xxxxxxx";
  var EMAILJS_PUBLIC_KEY = "xxxxxxxxxxxxxxxx";
  var INQUIRY_EMAIL = "lokesh@activeglobalimpex.com";

  // Ported from useInquiryForm.ts inquirySchema (zod)
  var RULES = {
    name: { min: 2, max: 80, required: true },
    company: { min: 2, max: 120, required: true },
    email: { email: true, required: true },
    phone: { min: 7, max: 20, required: true, pattern: /^\+?[\d\s\-()]{7,20}$/ },
    country: { min: 2, max: 60, required: true },
    product: { min: 2, max: 200, required: true },
    quantity: { min: 1, max: 100, required: true },
    message: { max: 1000, required: false }
  };

  document.addEventListener("DOMContentLoaded", function () {
    var form = document.getElementById("contact-form");
    if (!form) return;

    if (window.emailjs && EMAILJS_PUBLIC_KEY.indexOf("xxxx") === -1) {
      window.emailjs.init({ publicKey: EMAILJS_PUBLIC_KEY });
    }

    var successEl = document.getElementById("form-success");
    var errorBanner = form.querySelector(".form-error-banner");
    var submitBtn = form.querySelector("[type='submit']");
    var lang = document.documentElement.getAttribute("lang") === "id" ? "id" : "en";
    var t = (window.AGI_I18N && window.AGI_I18N.dict[lang]) || {};

    form.addEventListener("submit", function (e) {
      e.preventDefault();
      hideErrorBanner();

      var valid = true;
      Object.keys(RULES).forEach(function (name) {
        var field = form.elements[name];
        if (!field) return;
        if (!validateField(field, RULES[name], t)) valid = false;
      });

      if (!valid) {
        var firstError = form.querySelector(".has-error input, .has-error textarea");
        if (firstError) firstError.focus();
        return;
      }

      if (!window.emailjs || EMAILJS_PUBLIC_KEY.indexOf("xxxx") !== -1) {
        showErrorBanner(t["contact.form.errorTitle"], t["contact.form.errorBody"]);
        console.warn("EmailJS is not configured. Set EMAILJS_SERVICE_ID / TEMPLATE_ID / PUBLIC_KEY in js/form.js.");
        return;
      }

      setLoading(true);

      window.emailjs
        .send(EMAILJS_SERVICE_ID, EMAILJS_TEMPLATE_ID, {
          from_name: form.elements.name.value.trim(),
          from_email: form.elements.email.value.trim(),
          phone: form.elements.phone.value.trim(),
          company: form.elements.company.value.trim(),
          country: form.elements.country.value.trim(),
          product: form.elements.product.value.trim(),
          quantity: form.elements.quantity.value.trim(),
          message: form.elements.message.value.trim(),
          to_email: INQUIRY_EMAIL
        })
        .then(function () {
          form.hidden = true;
          if (successEl) successEl.hidden = false;
          form.reset();
        })
        .catch(function (err) {
          console.error("EmailJS error:", err);
          showErrorBanner(t["contact.form.errorTitle"], t["contact.form.errorBody"]);
        })
        .finally(function () {
          setLoading(false);
        });
    });

    Object.keys(RULES).forEach(function (name) {
      var field = form.elements[name];
      if (!field) return;
      field.addEventListener("blur", function () {
        validateField(field, RULES[name], t);
      });
    });

    var sendAnotherBtn = document.getElementById("send-another");
    if (sendAnotherBtn) {
      sendAnotherBtn.addEventListener("click", function () {
        if (successEl) successEl.hidden = true;
        form.hidden = false;
      });
    }

    function setLoading(isLoading) {
      if (!submitBtn) return;
      submitBtn.disabled = isLoading;
      submitBtn.classList.toggle("is-loading", isLoading);
    }

    function showErrorBanner(title, body) {
      if (!errorBanner) return;
      errorBanner.hidden = false;
      var strong = errorBanner.querySelector("strong");
      var span = errorBanner.querySelector("span");
      if (strong) strong.textContent = title || "Something went wrong.";
      if (span) span.textContent = body || "Please try again or reach us directly on WhatsApp.";
      errorBanner.scrollIntoView({ behavior: "smooth", block: "nearest" });
    }
    function hideErrorBanner() {
      if (errorBanner) errorBanner.hidden = true;
    }
  });

  function validateField(field, rule, t) {
    var wrapper = field.closest(".form-field");
    var errorEl = wrapper ? wrapper.querySelector(".field-error") : null;
    var value = field.value.trim();
    var message = "";

    if (rule.required && value.length === 0) {
      message = fieldRequiredMessage(field.name, t);
    } else if (value.length > 0 && rule.email) {
      var re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      if (!re.test(value)) message = "Please enter a valid email address";
    } else if (value.length > 0 && rule.pattern && !rule.pattern.test(value)) {
      message = "Please enter a valid international phone number";
    } else if (value.length > 0 && rule.min && value.length < rule.min) {
      message = fieldMinMessage(field.name);
    } else if (rule.max && value.length > rule.max) {
      message = "Message must be under " + rule.max + " characters";
    }

    if (wrapper) wrapper.classList.toggle("has-error", !!message);
    if (errorEl) errorEl.textContent = message;
    field.setAttribute("aria-invalid", message ? "true" : "false");
    return !message;
  }

  function fieldRequiredMessage(name, t) {
    var map = {
      name: "Name must be at least 2 characters",
      company: "Company name is required",
      email: "Please enter a valid email address",
      phone: "Please enter a valid phone number",
      country: "Please enter your country",
      product: "Please specify the product(s) you are interested in",
      quantity: "Please indicate the quantity required"
    };
    return map[name] || "This field is required";
  }
  function fieldMinMessage(name) {
    var map = {
      name: "Name must be at least 2 characters",
      company: "Company name is required",
      phone: "Please enter a valid phone number",
      country: "Please enter your country",
      product: "Please specify the product(s) you are interested in"
    };
    return map[name] || "Please provide a little more detail";
  }
})();
