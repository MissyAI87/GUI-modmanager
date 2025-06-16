# GUI Mod Manager for Sims 4

**GUI Mod Manager** is a Python app that combines ModFixer and ModFinder into one visual tool. It allows users to clean their Sims 4 Mods folder and search for new mods using a simple point-and-click interface.

---

## 💡 Features

- 🧼 One-click cleanup using ModFixer
- 🔍 Integrated mod search using ModFinder
- 🪟 Graphical interface (initially Tkinter, upgrading to PySimpleGUI or Gradio)
- 🧠 Built for future Ghost AI integration
- 🛠 Modular design – works even if scripts are updated independently

---
# GUI Mod Manager for Sims 4

**GUI Mod Manager** is a Python app that combines ModFixer and ModFinder into one visual tool. It allows users to clean their Sims 4 Mods folder and search for new mods using a simple point-and-click interface.

---

## 🖥️ How to Run

Make sure your virtual environment is activated:

```bash
source ~/sims4env/bin/activate
```

Then run the script:

```bash
python guimodmanager.py
```

The interface will open in a window or browser (depending on the GUI framework used). From there, you can:

- Click “Fix Mods” to run ModFixer
- Click “Find Mods” to launch the ModFinder tool
- View output directly in the interface or your working folder
---

## 📋 Future Plans

- Replace Tkinter with Gradio or PySimpleGUI for a modern UI
- Add log window to show script activity and results in real time
- Allow mod previews and descriptions in the interface
- One-click export of mod list to CSV
- Integrate directly with Ghost AI for voice-controlled automation
- Add “dry run” toggle to simulate changes before they’re applied

## 🙋 Author Notes

This project ties together two standalone tools (ModFixer and ModFinder) into a unified interface. It was built as part of a larger AI scripting ecosystem, with plans for future voice integration, modular automation, and enhanced user experience. Building this GUI taught me a lot about interface design, event handling, and script orchestration.

---

## 📝 License

This project is licensed under the MIT License.  
You are free to use, modify, and distribute this software.  
There is no warranty or liability for issues that may arise from use.
