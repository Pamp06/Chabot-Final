class Chatbox {
  constructor() {
    this.args = {
      openButton: document.querySelector(".chatbox__button"),
      chatBox: document.querySelector(".chatbox__support"),
      sendButton: document.querySelector(".send__button"),
    };

    this.state = false;
    this.messages = [];
    this.hasShownInitialMessage = false;
    this.enModoRecomendacion = false;
    this.recomendacionTemporal = null;
    this.esperandoCorreo = false;
    this.preguntandoPorCorreo = false;
  }

  display() {
    const { openButton, chatBox, sendButton } = this.args;

    openButton.addEventListener("click", () => {
      this.toggleState(chatBox);
      if (this.state && !this.hasShownInitialMessage) {
        this.showInitialMessage(chatBox);
        this.hasShownInitialMessage = true;
      }
      if (this.state) {
        setTimeout(() => this.agregarBotonRecomendacion(chatBox), 300);
      }
    });

    sendButton.addEventListener("click", () => this.onSendButton(chatBox));

    const node = chatBox.querySelector("input");
    node.addEventListener("keyup", ({ key }) => {
      if (key === "Enter") {
        this.onSendButton(chatBox);
      }
    });
  }

  scrollToBottom(chatbox) {
    const chatMessages = chatbox.querySelector(".chatbox__messages");
    chatMessages.scrollTop = chatMessages.scrollHeight;
  }

  showInitialMessage(chatbox) {
    fetch($SCRIPT_ROOT + "/initial_message")
      .then((r) => r.json())
      .then((r) => {
        const botResponse = r.raw_html || r.answer;
        let msg = {
          name: "Paulina",
          message: botResponse,
          isHtml: !!r.raw_html,
        };
        this.messages.push(msg);
        this.updateChatText(chatbox);
        this.scrollToBottom(chatbox);

        if (r.buttons && Array.isArray(r.buttons)) {
          this.generateButtons(chatbox, r.buttons);
        }
      })
      .catch((error) => {
        console.error("Error al obtener mensaje inicial:", error);
        let msg = {
          name: "Paulina",
          message:
            "¡Hola! Soy Paulina, tu asistente virtual. ¿En qué puedo ayudarte hoy?",
          isHtml: false,
        };
        this.messages.push(msg);
        this.updateChatText(chatbox);
        this.scrollToBottom(chatbox);

        this.generateButtons(chatbox, [{ text: "Empezar", value: "Empezar" }]);
      });
  }

  toggleState(chatbox) {
    this.state = !this.state;

    if (this.state) {
      chatbox.classList.add("chatbox--active");
      setTimeout(() => this.scrollToBottom(chatbox), 100);
    } else {
      chatbox.classList.remove("chatbox--active");
    }
  }

  onSendButton(chatbox, message = null) {
    const input = chatbox.querySelector("input");
    let text1 = message || input.value.trim();
    if (text1 === "") return;

    if (this.enModoRecomendacion) {
      if (this.preguntandoPorCorreo) {
        // Procesar respuesta Si/No
        if (
          text1.toLowerCase() === "sí" ||
          text1.toLowerCase() === "si" ||
          text1 === "si_correo"
        ) {
          // Limpiar botones antes de pedir el correo
          const botonesContainer = chatbox.querySelector("#botones-container");
          botonesContainer.innerHTML = "";
          this.pedirCorreoElectronico(chatbox);
        } else if (text1.toLowerCase() === "no" || text1 === "no_correo") {
          // Limpiar botones antes de finalizar
          const botonesContainer = chatbox.querySelector("#botones-container");
          botonesContainer.innerHTML = "";
          this.finalizarRecomendacion(chatbox, "");
        }
        this.preguntandoPorCorreo = false;
        input.value = "";
        return;
      }

      if (this.esperandoCorreo) {
        const correo = text1;
        if (this.validarCorreo(correo)) {
          // Limpiar botones si el correo es válido
          const botonesContainer = chatbox.querySelector("#botones-container");
          botonesContainer.innerHTML = "";
          this.finalizarRecomendacion(chatbox, correo);
        } else {
          const msgError = {
            name: "Paulina",
            message:
              "❌ El formato del correo no es válido. ¿Deseas intentarlo de nuevo?",
            isHtml: false,
          };
          // Limpiar botones antes de mostrar los nuevos
          const botonesContainer = chatbox.querySelector("#botones-container");
          botonesContainer.innerHTML = "";
          this.generateButtons(chatbox, [
            { text: "Sí", value: "si_correo" },
            { text: "No", value: "no_correo" },
          ]);
          this.messages.push(msgError);
          this.updateChatText(chatbox);
          this.preguntandoPorCorreo = true;
        }
        input.value = "";
        this.esperandoCorreo = false;
        return;
      }

      // Primera parte: recibir recomendación
      this.recomendacionTemporal = text1;
      this.preguntarPorCorreo(chatbox);
      input.value = "";
      return;
    }

    // Flujo normal de conversación
    const msg1 = { name: "Usuario", message: text1 };
    this.messages.push(msg1);
    this.updateChatText(chatbox);
    this.scrollToBottom(chatbox);

    fetch($SCRIPT_ROOT + "/predict", {
      method: "POST",
      body: JSON.stringify({ message: text1 }),
      mode: "cors",
      headers: {
        "Content-Type": "application/json",
      },
    })
      .then((r) => r.json())
      .then((r) => {
        const botResponse = r.raw_html || r.answer;
        let msg2 = {
          name: "Paulina",
          message: botResponse,
          isHtml: !!r.raw_html,
        };
        this.messages.push(msg2);
        this.updateChatText(chatbox);
        this.scrollToBottom(chatbox);

        if (r.buttons && Array.isArray(r.buttons)) {
          this.generateButtons(chatbox, r.buttons);
        }

        input.value = "";
        input.focus();
      })
      .catch((error) => {
        console.error("Error:", error);
        input.value = "";
        input.focus();
      });
  }

  updateChatText(chatbox) {
    var html = "";
    this.messages
      .slice()
      .reverse()
      .forEach((item) => {
        let messageContent = item.isHtml
          ? this.formatHtmlMessage(item.message)
          : this.escapeHtml(item.message);

        // Mantener saltos de línea en el HTML renderizado
        messageContent = messageContent.replace(/\n/g, "<br>");

        if (item.name === "Paulina") {
          html += `<div class="messages__item messages__item--visitor">${messageContent}</div>`;
        } else {
          html += `<div class="messages__item messages__item--operator">${messageContent}</div>`;
        }
      });

    const chatmessage = chatbox.querySelector(".chatbox__messages");
    chatmessage.innerHTML = html;
  }

  formatHtmlMessage(html) {
    html = html.replace(/<br\s*\/?>/gi, "\n").replace(/&nbsp;/gi, " ");

    const allowedTags = {
      b: true,
      strong: true,
      i: true,
      em: true,
      u: true,
      p: true,
    };

    return html.replace(/<\/?([a-z][a-z0-9]*)\b[^>]*>/gi, (match, tag) =>
      allowedTags[tag.toLowerCase()] ? match : ""
    );
  }

  escapeHtml(text) {
    const div = document.createElement("div");
    div.textContent = text;
    return div.innerHTML;
  }

  generateButtons(chatbox, buttons) {
    const botonesContainer = chatbox.querySelector("#botones-container");
    botonesContainer.innerHTML = "";

    buttons.forEach((button) => {
      const btn = document.createElement("button");
      btn.textContent = button.text;
      btn.value = button.value;
      btn.classList.add("boton-opcion");

      if (button.value === "Empezar") {
        btn.classList.add("boton-seguir");
      }

      btn.addEventListener("click", () => {
        this.onSendButton(chatbox, button.value);
        botonesContainer.innerHTML = "";
      });

      botonesContainer.appendChild(btn);
    });

    this.scrollToBottom(chatbox);
  }

  agregarBotonRecomendacion(chatbox) {
    const footer = chatbox.querySelector(".chatbox__footer");

    if (footer.querySelector(".recomendacion__button")) {
      return;
    }

    const recomendacionBtn = document.createElement("button");
    recomendacionBtn.className = "recomendacion__button";
    recomendacionBtn.innerHTML = "💡 Enviar recomendación";
    recomendacionBtn.style.cssText = `
      position: absolute;
      bottom: -40px;
      left: 0;
      background: #581b98;
      color: white;
      border: none;
      padding: 8px 12px;
      border-radius: 15px;
      cursor: pointer;
      font-size: 0.8rem;
    `;

    recomendacionBtn.addEventListener("click", () => {
      if (this.enModoRecomendacion) return;
      recomendacionBtn.disabled = true;
      recomendacionBtn.style.opacity = "0.5";
      recomendacionBtn.style.pointerEvents = "none";
      this.iniciarFlujoRecomendacion(chatbox);
    });

    footer.style.position = "relative";
    footer.appendChild(recomendacionBtn);
  }

  iniciarFlujoRecomendacion(chatbox) {
    if (this.enModoRecomendacion) return;

    this.enModoRecomendacion = true;
    this.esperandoCorreo = false;
    this.preguntandoPorCorreo = false;

    const botonesContainer = chatbox.querySelector("#botones-container");
    botonesContainer.innerHTML = "";

    const input = chatbox.querySelector("input");
    input.value = "";
    input.placeholder = "Escribe tu recomendación aquí...";

    const msg = {
      name: "Paulina",
      message:
        "Por favor, siendo lo más breve posible 🎯 escribe tu recomendación en el cuadro de texto y presiona Enter o dale al botón de Enviar 😊",
      isHtml: false,
    };
    this.messages.push(msg);
    this.updateChatText(chatbox);
    this.scrollToBottom(chatbox);
  }

  preguntarPorCorreo(chatbox) {
    this.preguntandoPorCorreo = true;

    const msgPreguntaCorreo = {
      name: "Paulina",
      message:
        "¿Deseas proporcionar tu correo electrónico para que podamos contactarte? 📧🔔",
      isHtml: false,
    };

    this.messages.push(msgPreguntaCorreo);
    this.updateChatText(chatbox);
    this.scrollToBottom(chatbox);

    this.generateButtons(chatbox, [
      { text: "Sí", value: "si_correo" },
      { text: "No", value: "no_correo" },
    ]);
  }

  pedirCorreoElectronico(chatbox) {
    this.esperandoCorreo = true;

    const msgPideCorreo = {
      name: "Paulina",
      message: "Por favor ingresa tu correo electrónico 📩📩📩",
      isHtml: false,
    };

    this.messages.push(msgPideCorreo);
    this.updateChatText(chatbox);
    this.scrollToBottom(chatbox);

    const input = chatbox.querySelector("input");
    input.value = "";
    input.placeholder = "ejemplo@correo.com";
  }

  validarCorreo(correo) {
    const re = /\S+@\S+\.\S+/;
    return re.test(correo);
  }

  finalizarRecomendacion(chatbox, usuario) {
    fetch($SCRIPT_ROOT + "/guardar_recomendacion", {
      method: "POST",
      body: JSON.stringify({
        mensaje: this.recomendacionTemporal,
        usuario: usuario,
      }),
      headers: {
        "Content-Type": "application/json",
      },
    })
      .then((response) => response.json())
      .then((data) => {
        const msgAgradecimiento = {
          name: "Paulina",
          message:
            "✅ ¡Gracias por tu recomendación! 🎯 La tendremos en cuenta para mejorar 😄✨",
          isHtml: false,
        };
        this.messages.push(msgAgradecimiento);

        const msgBoton = {
          name: "Paulina",
          message: "¿En qué más puedo ayudarte?",
          isHtml: false,
          buttons: [
            {
              text: "Seguir conversación",
              value: "Empezar",
            },
          ],
        };
        this.messages.push(msgBoton);

        this.updateChatText(chatbox);
        this.enModoRecomendacion = false;
        this.esperandoCorreo = false;
        this.preguntandoPorCorreo = false;
        this.recomendacionTemporal = null;

        const recomendacionBtn = chatbox.querySelector(
          ".recomendacion__button"
        );
        if (recomendacionBtn) {
          recomendacionBtn.disabled = false;
          recomendacionBtn.style.opacity = "1";
          recomendacionBtn.style.pointerEvents = "auto";
        }

        this.generateButtons(chatbox, msgBoton.buttons);
        this.scrollToBottom(chatbox);

        // Restaurar estado
        const input = chatbox.querySelector("input");
        input.placeholder = "Escribe tu mensaje aquí...";
      })
      .catch((error) => {
        console.error("Error al enviar recomendación:", error);
      });
  }
}

// Control para mostrar/ocultar la ventana de chat
document.getElementById("buttonchat").addEventListener("click", function () {
  const chatwindow = document.getElementById("chatwindow");

  if (chatwindow.classList.contains("show")) {
    chatwindow.classList.remove("show");
    chatwindow.addEventListener(
      "transitionend",
      function () {
        if (!chatwindow.classList.contains("show")) {
          chatwindow.style.display = "none";
        }
      },
      { once: true }
    );
  } else {
    chatwindow.style.display = "block";
    requestAnimationFrame(() => {
      chatwindow.classList.add("show");
      setTimeout(() => {
        const chatbox = document.querySelector(".chatbox__support");
        const chatMessages = chatbox.querySelector(".chatbox__messages");
        chatMessages.scrollTop = chatMessages.scrollHeight;
      }, 300);
    });
  }
});

const chatbox = new Chatbox();
chatbox.display();
