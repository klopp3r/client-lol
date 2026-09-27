// @fork-plugin {"id":"sample","name":"Sample plugin","version":"1.0","author":"Telegram Fork","description":"Demo plugin showing what a plugin can do."}

fork.log("sample plugin loaded");

fork.addSection("Demo section");

fork.addSwitch(
    "greeting",
    "Show greeting",
    true,
    "A stored on/off value that survives restarts"
);

fork.addText(
    "nickname",
    "Your nickname",
    "friend",
    "A free text value that survives restarts"
);

fork.addAction("Say hello", "Calls back into the plugin", function () {
    var name = fork.getText("nickname", "friend");
    fork.log("greeting flag is " + fork.getFlag("greeting", true));
    fork.toast("Hello, " + name + "!");
});

fork.addInfo("Everything above was declared by this JavaScript file.");
