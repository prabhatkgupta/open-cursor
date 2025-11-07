# Setup your *Open-Cursor* in 5 mins

## Open-Cursor: Your Free, Open-Source AI Coding Assistant 🚀

### Introduction: Why Open-Cursor?

In the age of AI-powered coding assistants, tools like Cursor have revolutionized how developers write code. But what if you could have all that power without the monthly subscription, without sending your proprietary code to external servers, and with complete control over your development environment?

Enter **Open-Cursor** — an open-source alternative that runs entirely on your local machine. Here's why this matters:

🔒 **Privacy & Security**: Your code never leaves your machine. No cloud servers, no data collection, no privacy concerns.

💰 **Cost-Effective**: No monthly subscriptions or API costs. Once set up, it's completely free to use.

🎛️ **Full Control**: Choose your own models, customize system prompts, and modify the behavior to suit your needs.

🌍 **Open-Source**: Built on open-source technologies, giving you transparency and the freedom to modify.

Whether you're working on sensitive projects, want to avoid subscription fatigue, or simply believe in the open-source philosophy, Open-Cursor gives you enterprise-grade AI coding assistance on your terms.

---

## The Setup: A 3-Step Journey

Setting up Open-Cursor is straightforward and takes about 5–10 minutes. Let's break it down into three simple steps.

---

## Step 1: Setting Up Your Local AI Model with LM Studio 🧠

The first piece of the puzzle is getting a powerful language model running on your local machine. We'll use LM Studio for this – a user-friendly application that makes running LLMs locally a breeze.

### Download and Install LM Studio

Head over to [https://lmstudio.ai/](https://lmstudio.ai/) and download LM Studio for your operating system (macOS, Windows, or Linux).

### Choose Your Model

For this guide, we're using **Qwen2.5-Coder-7B-Instruct-MLX** – a 4-bit quantized model optimized for coding tasks. This model runs smoothly with under 10GB of RAM, making it accessible for most modern laptops.

🔗 **Model Link**: [Qwen2.5-Coder-7B-Instruct-4bit](https://huggingface.co/mlx-community/Qwen2.5-Coder-7B-Instruct-4bit)

![LM Studio Model Search](https://raw.githubusercontent.com/prabhatkgupta/open-cursor/main/assets/lm-studio-model-search.png)

Once you've opened LM Studio:
1. Navigate to the Model Search section
2. Search for "qwen2.5 coder 7b"
3. Download the 4-bit MLX version (approximately 4.3GB)

### Serve Your Model

After downloading, it's time to get your model up and running:

1. Go to the chat interface in LM Studio
2. Load the Qwen2.5-Coder model
3. Start the local server (it will run on `http://127.0.0.1:1234` by default)

![LM Studio Chat Interface](https://raw.githubusercontent.com/prabhatkgupta/open-cursor/main/assets/lm-studio-chat.png)

Test your setup by asking a simple coding question in the chat interface. If you get a coherent response, congratulations! 🎉

**✅ Your model is up. Now you got the 1st piece of the puzzle!**

---

## Step 2: Installing the Continue Plugin in PyCharm 🔌

Now that your AI brain is running, let's integrate it with your IDE. This tutorial uses PyCharm, but if you're using VS Code or another IDE, the underlying logic remains the same with minor UI differences.

### Install the Continue Plugin

Open PyCharm and navigate to:
**Settings → Plugins → Marketplace**

![PyCharm Plugins](https://raw.githubusercontent.com/prabhatkgupta/open-cursor/main/assets/pycharm-continue-plugin.png)

Search for **"Continue"** and install the plugin from:
🔗 [https://plugins.jetbrains.com/plugin/22707-continue](https://plugins.jetbrains.com/plugin/22707-continue)

### Configure the Plugin

The Continue plugin needs to know which model to use and how to communicate with it. I've prepared a ready-to-use configuration file that you can use without any modifications! 😃

**Configuration file**: [https://github.com/prabhatkgupta/open-cursor/blob/main/continue/config.yaml](https://github.com/prabhatkgupta/open-cursor/blob/main/continue/config.yaml)

This config file contains:
- Model specifications
- Chat templates
- System prompts
- API endpoints
- Version information

### Where to Place the Config

Copy the `config.yaml` file to your Continue configuration directory:

**macOS/Linux**: `~/.continue/config.yaml`

**Windows**: `C:\Users\YourUsername\.continue\config.yaml`

💡 **Tip**: If you're unsure about the exact path for your system, just ask ChatGPT: "Where is the Continue config file stored on [your OS]?" and you'll get the answer instantly!

Once done you will see model's in Continue's agent space

![Continue Plugin in Action](https://raw.githubusercontent.com/prabhatkgupta/open-cursor/main/assets/continue-plugin-action.png)

---

## Step 3: Creating the Router – The Critical Bridge 🌉

This is where the magic happens! The router is the critical component that ties everything together. It acts as a middleware that:

1. **Receives requests** from the Continue plugin
2. **Compiles and formats** them appropriately
3. **Routes them** to your local LM Studio model
4. **Streams the response** back token-by-token for that real-time coding experience

### The Router Code

I've created a Python-based router that handles all of this seamlessly:

🔗 **Router Code**: [https://github.com/prabhatkgupta/open-cursor/blob/main/scripts/router.py](https://github.com/prabhatkgupta/open-cursor/blob/main/scripts/router.py)

### Running the Router

Simply run the router script:

```bash
python3 router.py
```

You'll see output like this confirming that streaming is working:

![Router Terminal Output](https://raw.githubusercontent.com/prabhatkgupta/open-cursor/main/assets/router-terminal.png)

The green text shows the streaming responses flowing from your local model through the router and back to your IDE. This streaming capability ensures you get that smooth, real-time experience just like the premium tools!

---

## Putting It All Together 🎯

Once all three components are running:

1. ✅ LM Studio serving your local model
2. ✅ Continue plugin installed and configured in PyCharm
3. ✅ Router script running and bridging the communication

You can now:
- Ask coding questions directly in your IDE
- Get AI-powered code completions
- Request refactoring suggestions
- Generate code snippets
- Debug with AI assistance

All of this happens locally, privately, and at no cost! 🎉

**Demo explaining the usage**: [LINK](https://drive.google.com/file/d/1qlSAt8Py7Hz5mvhomrupjTrUkTkGWNP8/view?usp=sharing) 😃

---

## Customization & Advanced Usage 🛠️

The beauty of Open-Cursor is its flexibility:

### Try Different Models
- Want faster responses? Try smaller models
- Need more accuracy? Download larger models
- Specialized in a language? Find domain-specific models on Hugging Face

### Modify System Prompts
Edit the `config.yaml` to change how the AI responds:
- Adjust verbosity
- Set coding style preferences
- Add project-specific context

### Run Multiple Models
You can serve different models for different purposes:
- One for code generation
- Another for documentation
- A third for debugging

---

## Troubleshooting Common Issues 🔧

**Model not responding?**
- Check if LM Studio server is running
- Verify the port numbers match in your config

**Slow responses?**
- Consider using a smaller model
- Check your RAM usage
- Ensure no other heavy processes are running

**Router connection errors?**
- Confirm the router script is running
- Check firewall settings
- Verify API endpoints in config.yaml

---

## What's Next? 🚀

This is just the beginning! Here are some ways to extend your Open-Cursor setup:

- **Add more models** for different tasks
- **Integrate with Git** for commit message generation
- **Create custom prompts** for your team's coding standards
- **Build additional tools** on top of the router

---

## Resources & Links 📚

- **GitHub Repository**: [https://github.com/prabhatkgupta/open-cursor](https://github.com/prabhatkgupta/open-cursor)
- **LM Studio**: [https://lmstudio.ai/](https://lmstudio.ai/)
- **Continue Plugin**: [https://plugins.jetbrains.com/plugin/22707-continue](https://plugins.jetbrains.com/plugin/22707-continue)
- **Qwen2.5-Coder Model**: [https://huggingface.co/mlx-community/Qwen2.5-Coder-7B-Instruct-4bit](https://huggingface.co/mlx-community/Qwen2.5-Coder-7B-Instruct-4bit)

---

## Conclusion: Code Freely, Code Privately 🌟

Open-Cursor represents more than just a free alternative to commercial tools – it's a statement about software freedom, privacy, and the democratization of AI technology. By running everything locally, you maintain complete control over your development environment while getting enterprise-grade AI assistance.

The initial setup might take a few minutes, but the benefits – privacy, cost savings, and customization – make it worthwhile for any developer serious about their craft.

Give it a try, and experience the future of coding on your own terms! 💻✨

---

**Found this helpful? ⭐ Star the repository and share it with fellow developers who value open-source and privacy!**

---

*Have questions or want to contribute? Open an issue or PR on the [GitHub repository](https://github.com/prabhatkgupta/open-cursor). Let's build the future of open-source AI coding tools together!*
