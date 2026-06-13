const chat = document.getElementById("chat");
const form = document.getElementById("form");
const input = document.getElementById("input");
const sendBtn = document.getElementById("send");
const tempSlider = document.getElementById("temperature");
const lenSlider = document.getElementById("maxLen");
const tempVal = document.getElementById("tempVal");
const lenVal = document.getElementById("lenVal");

// 슬라이더 값 표시 동기화
tempSlider.addEventListener("input", () => (tempVal.textContent = tempSlider.value));
lenSlider.addEventListener("input", () => (lenVal.textContent = lenSlider.value));

// 말풍선 추가 헬퍼
function addBubble(role, html, extraClass = "") {
  const msg = document.createElement("div");
  msg.className = `msg ${role}`;
  const bubble = document.createElement("div");
  bubble.className = `bubble ${extraClass}`;
  bubble.innerHTML = html;
  msg.appendChild(bubble);
  chat.appendChild(msg);
  chat.scrollTop = chat.scrollHeight;
  return bubble;
}

function escapeHtml(s) {
  const div = document.createElement("div");
  div.textContent = s;
  return div.innerHTML;
}

form.addEventListener("submit", async (e) => {
  e.preventDefault();
  const text = input.value.trim();
  if (!text) return;

  addBubble("user", escapeHtml(text));
  input.value = "";
  sendBtn.disabled = true;

  const loading = addBubble("bot", "생성 중...", "loading");

  try {
    const res = await fetch("/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        text,
        temperature: parseFloat(tempSlider.value),
        max_new_tokens: parseInt(lenSlider.value, 10),
      }),
    });

    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      throw new Error(err.detail || `오류 (${res.status})`);
    }

    const data = await res.json();
    // 입력 부분 + 생성된 부분(강조)으로 표시
    loading.className = "bubble";
    loading.innerHTML =
      escapeHtml(data.input) + `<span class="gen">${escapeHtml(data.generated)}</span>`;
  } catch (err) {
    loading.className = "bubble";
    loading.textContent = "⚠️ " + err.message;
  } finally {
    sendBtn.disabled = false;
    input.focus();
  }
});
