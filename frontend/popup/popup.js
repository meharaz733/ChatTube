const chatContainer = document.getElementById("chat-container");
const input = document.getElementById("message-input");
const sendBtn = document.getElementById("send-btn");
const startBtn = document.getElementById("start-btn");
const startContainer = document.getElementById("start");
const inputArea = document.getElementById("input-area");

let sessionID = null
let videoID = null

function addMessage(text, sender){
  const msg = document.createElement("div");
  msg.classList.add("message", sender);
  msg.textContent = text;
  chatContainer.appendChild(msg);
  chatContainer.scrollTop = chatContainer.scrollHeight;
}

startBtn.addEventListener("click", async () => {
  const [tab] = await chrome.tabs.query({
    active:true,
    currentWindow: true
  });
  const video_url = tab.url;
  console.log(video_url)
  try{
    const response = await fetch(
      "http://127.0.0.1:8000/start",
      {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
          "video_url": video_url
        })
      }
    );
    const data = await response.json();
    sessionID = data.sessionID;
    videoID = data.videoID;

    startContainer.style.display = "none";
    chatContainer.style.display = "flex";
    inputArea.style.display = "flex";
  }
  catch (error){
    console.log("Error: " + error.message)
  }
});


sendBtn.addEventListener("click", async () => {
  const text = input.value.trim();
  if(!text || !sessionID || !videoID) return;

  addMessage(text, "user");
  input.value = "";

  try{
    const response = await fetch("http://127.0.0.1:8000/chat", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        "videoID": videoID,
        "sessionID": sessionID,
        "user_query": text
        })
    });

    const data = await response.json();
    const reply = data.aiAnswer || "No response from the server";
    addMessage(reply, "ai")
  }
  catch (error){
    addMessage("Connection Error!", 'ai');
  }
});

input.addEventListener("keypress", (e) => {
  if (e.key === "Enter") sendBtn.click();
});
