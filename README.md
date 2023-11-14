# Ollama Web UI: A User-Friendly Web Interface for Chat Interactions 👋

![GitHub stars](https://img.shields.io/github/stars/ollama-webui/ollama-webui?style=social)
![GitHub forks](https://img.shields.io/github/forks/ollama-webui/ollama-webui?style=social)
![GitHub watchers](https://img.shields.io/github/watchers/ollama-webui/ollama-webui?style=social)
![GitHub repo size](https://img.shields.io/github/repo-size/ollama-webui/ollama-webui)
![GitHub language count](https://img.shields.io/github/languages/count/ollama-webui/ollama-webui)
![GitHub top language](https://img.shields.io/github/languages/top/ollama-webui/ollama-webui)
![GitHub last commit](https://img.shields.io/github/last-commit/ollama-webui/ollama-webui?color=red)
![Hits](https://hits.seeyoufarm.com/api/count/incr/badge.svg?url=https%3A%2F%2Fgithub.com%2Follama-webui%2Follama-wbui&count_bg=%2379C83D&title_bg=%23555555&icon=&icon_color=%23E7E7E7&title=hits&edge_flat=false)
[![Discord](https://img.shields.io/badge/Discord-Ollama_Web_UI-blue?logo=discord&logoColor=white)](https://discord.gg/5rJgQTnV4s)
[![](https://img.shields.io/static/v1?label=Sponsor&message=%E2%9D%A4&logo=GitHub&color=%23fe8e86)](https://github.com/sponsors/tjbck)

ChatGPT-Style Web Interface for Ollama 🦙

![Ollama Web UI Demo](./demo.gif)

## Features ⭐

- 🖥️ **Intuitive Interface**: Our chat interface takes inspiration from ChatGPT, ensuring a user-friendly experience.

- 📱 **Responsive Design**: Enjoy a seamless experience on both desktop and mobile devices.

- ⚡ **Swift Responsiveness**: Enjoy fast and responsive performance.

- 🚀 **Effortless Setup**: Install seamlessly using Docker for a hassle-free experience.

- 💻 **Code Syntax Highlighting**: Enjoy enhanced code readability with our syntax highlighting feature.

- ✒️🔢 **Full Markdown and LaTeX Support**: Elevate your LLM experience with comprehensive Markdown and LaTeX capabilities for enriched interaction.

- 📥🗑️ **Download/Delete Models**: Easily download or remove models directly from the web UI.

- 🤖 **Multiple Model Support**: Seamlessly switch between different chat models for diverse interactions.

- ⚙️ **Many Models Conversations**: : Effortlessly engage with various models simultaneously, harnessing their unique strengths for optimal responses. Enhance your experience by leveraging a diverse set of models in parallel.

- 🤝 **OpenAI Model Integration**: Seamlessly utilize OpenAI models alongside Ollama models for a versatile conversational experience.

- 🔄 **Regeneration History Access**: Easily revisit and explore your entire regeneration history.

- 📜 **Chat History**: Effortlessly access and manage your conversation history.

- 📤📥 **Import/Export Chat History**: Seamlessly move your chat data in and out of the platform.

- 🗣️ **Voice Input Support**: Engage with your model through voice interactions; enjoy the convenience of talking to your model directly. Additionally, explore the option for sending voice input automatically after 3 seconds of silence for a streamlined experience.

- ⚙️ **Fine-Tuned Control with Advanced Parameters**: Gain a deeper level of control by adjusting parameters such as temperature and defining your system prompts to tailor the conversation to your specific preferences and needs.

- 🔗 **External Ollama Server Connection**: Seamlessly link to an external Ollama server hosted on a different address by configuring the environment variable during the Docker build phase. Additionally, you can also set the external server connection URL from the web UI post-build.

- 🌟 **Continuous Updates**: We are committed to improving Ollama Web UI with regular updates and new features.

## How to Install 🚀

### Prerequisites

Make sure you have the latest version of Ollama installed before proceeding with the installation. You can find the latest version of Ollama at [https://ollama.ai/](https://ollama.ai/).

#### Installing Both Ollama and Ollama Web UI Using Docker Compose

If you don't have Ollama installed, you can also use the provided Docker Compose file for a hassle-free installation. Simply run the following command:

```bash
docker compose up --build
```

This command will install both Ollama and Ollama Web UI on your system. Ensure to modify the `compose.yaml` file for GPU support if needed.

#### Checking Ollama

After installing, verify that Ollama is running by accessing the following link in your web browser: [http://127.0.0.1:11434/](http://127.0.0.1:11434/). Note that the port number may differ based on your system configuration.

#### Accessing Ollama Web Interface over LAN

If you want to access the Ollama web interface over LAN, for example, from your phone, run Ollama using the following command:

```bash
OLLAMA_HOST=0.0.0.0 OLLAMA_ORIGINS=* ollama serve
```

In case you encounter any issues running the command and encounter errors, ensure to turn off any existing Ollama service that might be running in the background before retrying.

If you're running Ollama via Docker:

```bash
docker run -d -v ollama:/root/.ollama -p 11434:11434 -e OLLAMA_ORIGINS="*" --name ollama ollama/ollama
```

### Using Docker 🐳

If Ollama is hosted on your local machine, run the following command:

```bash
docker run -d -p 3000:8080 --name ollama-webui --restart always ghcr.io/ollama-webui/ollama-webui:main
```

Alternatively, if you prefer to build the container yourself, use the following command:

```bash
docker build --build-arg OLLAMA_API_BASE_URL='' -t ollama-webui .
docker run -d -p 3000:8080 --name ollama-webui --restart always ollama-webui
```

Your Ollama Web UI should now be hosted at [http://localhost:3000](http://localhost:3000). Enjoy! 😄

#### Connecting to Ollama on a Different Server

If Ollama is hosted on a server other than your local machine, change `OLLAMA_API_BASE_URL` to match:

```bash
docker build --build-arg OLLAMA_API_BASE_URL='https://example.com/api' -t ollama-webui .
docker run -d -p 3000:8080 --name ollama-webui --restart always ollama-webui
```

## How to Build for Static Deployment

1. Install `node`

   ```sh
   # Mac, Linux
   curl https://webi.sh/node@lts | sh
   source ~/.config/envman/PATH.env
   ```

   ```pwsh
   # Windows
   curl.exe https://webi.ms/node@lts | powershell
   ```

2. Clone & Enter the project
   ```sh
   git clone https://github.com/ollama-webui/ollama-webui.git
   pushd ./ollama-webui/
   ```
3. Create and edit `.env`
   ```sh
   cp -RPp example.env .env
   ```
4. Run in dev mode, or build the site for deployment
   - Test in Dev mode:
     ```sh
     npm run dev
     ```
   - Build for Deploy: \
     (`PUBLIC_API_BASE_URL` will overwrite the value in `.env`)
     ```sh
     PUBLIC_API_BASE_URL='https://example.com/api' npm run build
     ```
5. Test the build with `caddy` (or the server of your choice)

   ```sh
   curl https://webi.sh/caddy | sh

   PUBLIC_API_BASE_URL='https://localhost/api' npm run build
   caddy run --envfile .env --config ./Caddyfile.localhost
   ```

## Troubleshooting

See [TROUBLESHOOTING.md](/TROUBLESHOOTING.md) for information on how to troubleshoot and/or join our [Ollama Web UI Discord community](https://discord.gg/5rJgQTnV4s).

## What's Next? 🚀

### To-Do List 📝

Here are some exciting tasks on our to-do list:

- 🧪 **Research-Centric Features**: Empower researchers in the fields of LLM and HCI with a comprehensive web UI for conducting user studies. Stay tuned for ongoing feature enhancements (e.g., surveys, analytics, and participant tracking) to facilitate their research.
- 📈 **User Study Tools**: Providing specialized tools, like heat maps and behavior tracking modules, to empower researchers in capturing and analyzing user behavior patterns with precision and accuracy.
- 🌐 **Web Browser Extension**: Seamlessly integrate our services into your browsing experience with our convenient browser extension.
- 📚 **Enhanced Documentation**: Elevate your setup and customization experience with improved, comprehensive documentation.

Feel free to contribute and help us make Ollama Web UI even better! 🙌

## Supporters ✨

A big shoutout to our amazing supporters who's helping to make this project possible! 🙏

## Platinum Sponsors 🤍

- [Prof. Lawrence Kim @ SFU](https://www.lhkim.com/)

## License 📜

This project is licensed under the [MIT License](LICENSE) - see the [LICENSE](LICENSE) file for details. 📄

## Support 💬

If you have any questions, suggestions, or need assistance, please open an issue or join our
[Ollama Web UI Discord community](https://discord.gg/5rJgQTnV4s) or
[Ollama Discord community](https://discord.gg/ollama) to connect with us! 🤝

---

Created by [Timothy J. Baek](https://github.com/tjbck) - Let's make Ollama Web UI even more amazing together! 💪
