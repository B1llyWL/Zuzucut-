<h1 align="center">Zuzucut Bot</h1>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Aiogram-2.25-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white" alt="Aiogram">
  <img src="https://img.shields.io/badge/Telegram%20Bot-26A5E4?style=for-the-badge&logo=telegram&logoColor=white" alt="Telegram Bot">
</p>

<p align="center">
  🎨 <b>Zuzucut Bot</b> — Telegram bot for collecting art commissions. <br>
  It guides clients through a step‑by‑step form and sends the completed request to the artist.
</p>

<p align="center">
  <!-- Telegram Bot Link -->
  <a href="https://t.me/Zuzucutbot" target="_blank">
    <img src="https://img.shields.io/badge/Open%20in-Telegram-26A5E4?style=for-the-badge&logo=telegram" alt="Open in Telegram">
  </a>
</p>

---

<h2>📸 Screenshot</h2>

## Screenshots

<div align="center">
  <img src="https://github.com/user-attachments/assets/4bd7bad0-8690-44a3-a93b-7789c574d1c2" 
       alt="Bot interface"
       width="651"
       style="max-width:100%; height:auto; border-radius:8px; box-shadow:0 4px 12px rgba(0,0,0,0.1);">
</div>

<details>
<summary>Admin</summary>
<div style="display: flex; flex-wrap: wrap; gap: 10px; margin-top: 10px;">
  <img width="48%" alt="admin"
  <img width="48%" alt="admin_1" src="https://github.com/user-attachments/assets/2b05d758-7600-4334-891d-399a3d6d1a18" />
  <img width="48%" alt="admin_templates" src="https://github.com/user-attachments/assets/3d6120dd-c9a6-4e8e-bfd6-8398c968b032" />
  <img width="48%" alt="admin_command" src="https://github.com/user-attachments/assets/6ac99a2c-c73d-4992-a13d-4cf4fce3d9e6" />
  <img width="48%" alt="admin_2"
  <img width="48%" alt="client_menu_admin" src="https://github.com/user-attachments/assets/ed0d9ad2-e9d5-4c01-9890-1038d2222d09" />

</div>
</details>

<details>
<summary>User</summary>
<div style="display: flex; flex-wrap: wrap; gap: 10px; margin-top: 10px;">
  <img width="48%" 
  <img width="48%" 
</div>
</details>

<h3>📋 What the bot collects</h3>

<table style="width:80%; border-collapse:collapse;">
  <tr>
    <th style="background:#f2f2f2; padding:8px; border:1px solid #ddd;">Step</th>
    <th style="background:#f2f2f2; padding:8px; border:1px solid #ddd;">Information</th>
  </tr>
  <tr>
    <td style="padding:8px; border:1px solid #ddd;">1</td>
    <td style="padding:8px; border:1px solid #ddd;">Name</td>
  </tr>
  <tr>
    <td style="padding:8px; border:1px solid #ddd;">2</td>
    <td style="padding:8px; border:1px solid #ddd;">Username (for delivery)</td>
  </tr>
  <tr>
    <td style="padding:8px; border:1px solid #ddd;">3</td>
    <td style="padding:8px; border:1px solid #ddd;">Type of work (full art / sketch)</td>
  </tr>
  <tr>
    <td style="padding:8px; border:1px solid #ddd;">4</td>
    <td style="padding:8px; border:1px solid #ddd;">Background style (flat color, simple rendering, collage)</td>
  </tr>
  <tr>
    <td style="padding:8px; border:1px solid #ddd;">5</td>
    <td style="padding:8px; border:1px solid #ddd;">Deadline (with +30% for urgency)</td>
  </tr>
  <tr>
    <td style="padding:8px; border:1px solid #ddd;">6</td>
    <td style="padding:8px; border:1px solid #ddd;">Extra factors (second character, excessive detail, complex angle)</td>
  </tr>
  <tr>
    <td style="padding:8px; border:1px solid #ddd;">7</td>
    <td style="padding:8px; border:1px solid #ddd;">Additional comments</td>
  </tr>
   <tr>
    <td style="padding:8px; border:1px solid #ddd;">8</td>
    <td style="padding:8px; border:1px solid #ddd;">References</td>
  </tr>
</table>

<h2>🤖 Bot Commands & Features</h2>

<ul style="display:inline-block; text-align:left;">
  <li><code>/start</code> – welcome message and main menu</li>
  <li><code>/help</code> – get assistance</li>
  <li><code>/contact</code> – contact the developer and artist</li>
  <li><code>/register</code> – start a new art commission request</li>
  <li><b>Interactive buttons:</b>
    <ul>
      <li>❓ How to order an art</li>
      <li>💰 Payment info (Sberbank, RUB only)</li>
      <li>💵 Price list (detailed pricing)</li>
      <li>🖼️ Examples of works (link to portfolio)</li>
      <li>⏳ Typical deadlines</li>
      <li>⭐ Client reviews</li>
    </ul>
  </li>
</ul>

<h2>🚀 How to Use</h2>

<p>
  1. Open Telegram and search for <code>@Zuzucutbot</code>.<br>
  2. Start the bot with <code>/start</code>.<br>
  3. Use the menu buttons or <code>/register</code> to place an order.<br>
  4. Follow the step‑by‑step questionnaire – your request will be sent directly to the artist.
</p>

<h2>⚙️ Installation (for developers)</h2>

<p>
  <i>Want to run your own instance?</i>
</p>

<pre style="background:#f6f8fa; padding:15px; border-radius:8px; max-width:800px; margin:0 auto;"><code># 1. Clone the repository
git clone https://github.com/yourusername/zuzucut-bot.git
cd zuzucut-bot

# 2. Install dependencies
pip install -r requirements.txt

# 3. Create a .env file with your bot token
echo "BOT_TOKEN=your_telegram_bot_token" > .env

# 4. Run the bot
python bot.py</code></pre>


