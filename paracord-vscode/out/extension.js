"use strict";
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    var desc = Object.getOwnPropertyDescriptor(m, k);
    if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
      desc = { enumerable: true, get: function() { return m[k]; } };
    }
    Object.defineProperty(o, k2, desc);
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || (function () {
    var ownKeys = function(o) {
        ownKeys = Object.getOwnPropertyNames || function (o) {
            var ar = [];
            for (var k in o) if (Object.prototype.hasOwnProperty.call(o, k)) ar[ar.length] = k;
            return ar;
        };
        return ownKeys(o);
    };
    return function (mod) {
        if (mod && mod.__esModule) return mod;
        var result = {};
        if (mod != null) for (var k = ownKeys(mod), i = 0; i < k.length; i++) if (k[i] !== "default") __createBinding(result, mod, k[i]);
        __setModuleDefault(result, mod);
        return result;
    };
})();
Object.defineProperty(exports, "__esModule", { value: true });
exports.activate = activate;
exports.deactivate = deactivate;
const vscode = __importStar(require("vscode"));
function activate(context) {
    console.log('Paracord extension is now active!');
    // Completion Provider - Autocomplete saat ketik $
    const completionProvider = vscode.languages.registerCompletionItemProvider('paracord', {
        provideCompletionItems(document, position) {
            const linePrefix = document.lineAt(position).text.substr(0, position.character);
            // Cek apakah user baru ketik $
            if (!linePrefix.endsWith('$')) {
                return undefined;
            }
            const scope = getScope(document, position);
            return getCompletionItems(scope);
        }
    }, '$' // Trigger autocomplete saat ketik $
    );
    // Hover Provider - Info saat hover keyword
    const hoverProvider = vscode.languages.registerHoverProvider('paracord', {
        provideHover(document, position) {
            const range = document.getWordRangeAtPosition(position, /\$[a-zA-Z_][a-zA-Z0-9_]*/);
            if (!range) {
                return;
            }
            const word = document.getText(range);
            const info = getHoverInfo(word);
            if (info) {
                return new vscode.Hover(new vscode.MarkdownString(info));
            }
        }
    });
    context.subscriptions.push(completionProvider, hoverProvider);
}
function deactivate() { }
function getScope(document, position) {
    const text = document.getText();
    const offset = document.offsetAt(position);
    const beforeText = text.substring(0, offset);
    // Check context blocks
    const contexts = [
        { keyword: '$bot', scope: 'bot' },
        { keyword: '$addCommand', scope: 'command' },
        { keyword: '$addSlashCommand', scope: 'slash' },
        { keyword: '$newButton', scope: 'button' },
        { keyword: '$newSelectMenu', scope: 'select' },
        { keyword: '$newModal', scope: 'modal' },
        { keyword: '$event', scope: 'event' },
        { keyword: '$embed', scope: 'embed' }
    ];
    let currentScope = 'global';
    let maxIndex = -1;
    for (const ctx of contexts) {
        const lastIndex = beforeText.lastIndexOf(ctx.keyword + '(');
        if (lastIndex > maxIndex) {
            // Check if we're still inside this block
            let depth = 0;
            for (let i = lastIndex; i < offset; i++) {
                if (text[i] === '(')
                    depth++;
                if (text[i] === ')')
                    depth--;
            }
            if (depth > 0) {
                currentScope = ctx.scope;
                maxIndex = lastIndex;
            }
        }
    }
    return currentScope;
}
function getCompletionItems(scope) {
    const items = {
        global: [
            { name: '$bot', detail: 'Setup', doc: 'Bot configuration block' },
            { name: '$addCommand', detail: 'Command', doc: 'Create a text command' },
            { name: '$addSlashCommand', detail: 'Slash', doc: 'Create a slash command' },
            { name: '$newButton', detail: 'Component', doc: 'Define a button' },
            { name: '$newSelectMenu', detail: 'Component', doc: 'Define a select menu' },
            { name: '$newModal', detail: 'Component', doc: 'Define a modal' },
            { name: '$event', detail: 'Event', doc: 'Event handler' },
            { name: '$embed', detail: 'Embed', doc: 'Rich embed message' }
        ],
        bot: [
            { name: '$prefix', detail: 'Setup', doc: 'Command prefix (e.g., "!")' },
            { name: '$intents', detail: 'Setup', doc: 'Discord intents' },
            { name: '$status', detail: 'Setup', doc: 'Bot status (online/idle/dnd/offline)' },
            { name: '$activity', detail: 'Setup', doc: 'Bot activity (playing/watching/listening)' },
            { name: '$run', detail: 'Setup', doc: 'Start bot with token' }
        ],
        command: [
            { name: '$name', detail: 'Required', doc: 'Command name' },
            { name: '$sendMessage', detail: 'Response', doc: 'Send a message' },
            { name: '$useButton', detail: 'Component', doc: 'Add button' },
            { name: '$useSelectMenu', detail: 'Component', doc: 'Add select menu' },
            { name: '$cooldown', detail: 'Limit', doc: 'Add cooldown' },
            { name: '$setUserVar', detail: 'Variables', doc: 'Set user variable' },
            { name: '$getUserVar', detail: 'Variables', doc: 'Get user variable' }
        ],
        slash: [
            { name: '$name', detail: 'Required', doc: 'Command name' },
            { name: '$description', detail: 'Required', doc: 'Command description' },
            { name: '$slashCommandOption', detail: 'Option', doc: 'Add command option' },
            { name: '$sendMessage', detail: 'Response', doc: 'Send a message' },
            { name: '$useButton', detail: 'Component', doc: 'Add button' },
            { name: '$sendModal', detail: 'Component', doc: 'Send modal' }
        ],
        button: [
            { name: '$addButton', detail: 'Define', doc: 'Button definition: "id;label;style;value;emoji"' },
            { name: '$id', detail: 'Required', doc: 'Button ID for event' }
        ],
        select: [
            { name: '$id', detail: 'Required', doc: 'Select menu ID' },
            { name: '$placeholder', detail: 'Optional', doc: 'Placeholder text' },
            { name: '$addSelectMenuOption', detail: 'Option', doc: 'Add option: "id;label;value"' }
        ],
        modal: [
            { name: '$id', detail: 'Required', doc: 'Modal ID' },
            { name: '$title', detail: 'Required', doc: 'Modal title' },
            { name: '$addTextInput', detail: 'Input', doc: 'Add input: "id;label;min;max;placeholder"' }
        ],
        event: [
            { name: '$id', detail: 'Required', doc: 'Event ID matching button/select/modal' },
            { name: '$sendMessage', detail: 'Response', doc: 'Send message response' },
            { name: '$sendModal', detail: 'Response', doc: 'Send modal' },
            { name: '$if', detail: 'Conditional', doc: 'If condition: $if[$value==("...")]' },
            { name: '$elseif', detail: 'Conditional', doc: 'Else if condition' },
            { name: '$endif', detail: 'Conditional', doc: 'End if block' },
            { name: '$setUserVar', detail: 'Variables', doc: 'Set user variable' },
            { name: '$getUserVar', detail: 'Variables', doc: 'Get user variable' }
        ],
        embed: [
            { name: '$embedName', detail: 'Required', doc: 'Embed reference name' },
            { name: '$title', detail: 'Optional', doc: 'Embed title' },
            { name: '$description', detail: 'Optional', doc: 'Embed description' },
            { name: '$color', detail: 'Optional', doc: 'Color hex (#5865F2)' },
            { name: '$footer', detail: 'Optional', doc: 'Footer text' },
            { name: '$thumbnail', detail: 'Optional', doc: 'Thumbnail URL' },
            { name: '$image', detail: 'Optional', doc: 'Image URL' },
            { name: '$timestamp', detail: 'Optional', doc: 'Current timestamp' },
            { name: '$addField', detail: 'Optional', doc: 'Add field: "name;value;inline"' }
        ]
    };
    const scopeItems = items[scope] || items.global;
    return scopeItems.map(item => {
        const completion = new vscode.CompletionItem(item.name, vscode.CompletionItemKind.Function);
        completion.detail = item.detail;
        completion.documentation = new vscode.MarkdownString(item.doc);
        completion.insertText = item.name;
        return completion;
    });
}
function getHoverInfo(word) {
    const docs = {
        // Bot Setup
        '$bot': '**$bot** - Bot Configuration\n\n🤖 Main bot setup block.\n\nExample:\n```paracord\n$bot(\n  $prefix("!")\n  $intents("all")\n)\n```',
        '$prefix': '**$prefix** - Command Prefix\n\n⚙️ Set prefix for text commands.\n\n**Syntax:** `$prefix("character")`\n\nExample: `$prefix("!")` → Commands: !ping, !help',
        '$intents': '**$intents** - Bot Intents\n\n🔐 Configure Discord intents.\n\n**Options:**\n- `"all"` - All intents (recommended)\n- Specific intents\n\nExample: `$intents("all")`',
        '$status': '**$status** - Bot Status\n\n💚 Set bot online status.\n\n**Options:**\n- `"online"` - Green (online)\n- `"idle"` - Yellow (away)\n- `"dnd"` - Red (do not disturb)\n- `"offline"` - Gray (invisible)\n\nExample: `$status("online")`',
        '$activity': '**$activity** - Bot Activity\n\n🎮 Set bot activity status.\n\n**Syntax:** `$activity(type;"text")`\n\n**Types:**\n- `playing` - Playing X\n- `watching` - Watching X\n- `listening` - Listening to X\n- `streaming` - Streaming X\n- `competing` - Competing in X\n\nExample: `$activity(playing;"Paracord v2.8")`',
        '$run': '**$run** - Start Bot\n\n🚀 Start bot with token.\n\n**Syntax:** `$run("YOUR_TOKEN")`\n\n⚠️ **Important:**\n- Keep token secret!\n- Use environment variables in production\n- On Replit: Use `$run(BOT_TOKEN)` (no quotes)\n\nExample: `$run("MTEz...")`',
        // Commands
        '$addCommand': '**$addCommand** - Create Command\n\n📝 Create a text command (prefix-based).\n\n**Required:**\n- `$name` - Command name\n- `$sendMessage` - Response\n\nExample:\n```paracord\n$addCommand(\n  $name("ping")\n  $sendMessage("🏓 Pong!")\n)\n```\n\nUsage: `!ping`',
        '$name': '**$name** - Command Name\n\n🏷️ Set command name (without prefix).\n\n**Syntax:** `$name("commandname")`\n\n**Rules:**\n- No spaces\n- Lowercase recommended\n- No special characters\n\nExample: `$name("hello")` → Use with `!hello`',
        '$sendMessage': '**$sendMessage** - Send Message\n\n💬 Send text or embed message.\n\n**Syntax:**\n- Text: `$sendMessage("Hello!")`\n- Embed: `$sendMessage("embedName")`\n- With variables: `$sendMessage("Hello $username!")`\n\nExample:\n```paracord\n$sendMessage("👋 Hello $username!")\n```',
        // Slash Commands
        '$addSlashCommand': '**$addSlashCommand** - Slash Command\n\n⚡ Create a slash command (Discord native).\n\n**Required:**\n- `$name` - Command name\n- `$description` - Command description\n\nExample:\n```paracord\n$addSlashCommand(\n  $name("hello")\n  $description("Say hello")\n  $sendMessage("Hello!")\n)\n```\n\nUsage: `/hello`',
        '$description': '**$description** - Description\n\n📄 Command or embed description.\n\n**Slash Commands:** Required description for slash command\n**Embeds:** Embed body text\n\nExample:\n```paracord\n$description("This command says hello")\n```',
        '$slashCommandOption': '**$slashCommandOption** - Slash Option\n\n⚙️ Add option to slash command.\n\n**Syntax:** `$slashCommandOption("name;description;type;choices;required")`\n\n**Types:**\n- `input` - Text input\n- `number` - Number\n- `boolean` - True/False\n\nExample:\n```paracord\n$slashCommandOption("amount;Amount of coins;number;;true")\n```',
        // User Variables (v2.8)
        '$setUserVar': '**$setUserVar** - Set User Variable ⭐\n\n💾 Store data per user (v2.8).\n\n**Syntax:** `$setUserVar($userID;var_name;value)`\n\n**Operations:**\n- Direct: `100` - Set to 100\n- Add: `+50` - Add 50\n- Subtract: `-30` - Subtract 30\n- Multiply: `*2` - Double\n- Divide: `/2` - Half\n- Random: `+$random(10,100)` - Add random\n- String: `"text"` - Store text\n\nExample:\n```paracord\n$setUserVar($userID;coins;+100)\n$setUserVar($userID;name;$username)\n```\n\n📦 Storage: Saved in `uservars.json`',
        '$getUserVar': '**$getUserVar** - Get User Variable ⭐\n\n📊 Retrieve stored user data (v2.8).\n\n**Syntax:** `$getUserVar($userID;var_name)`\n\nReturns stored value or `"0"` if not set.\n\nExample:\n```paracord\nBalance: $getUserVar($userID;coins) coins\nLevel: $getUserVar($userID;level)\n```\n\n💡 **Tip:** Always use with `$setUserVar` first!',
        // Variables
        '$username': '**$username** - User Name\n\n👤 Display name of user.\n\nExample:\n```paracord\n$sendMessage("Hello $username!")\n```\n\nOutput: `Hello John!`',
        '$userID': '**$userID** - User ID\n\n🆔 Discord unique ID.\n\n**Uses:**\n- User variables: `$setUserVar($userID;...)`\n- Conditionals\n- Logging\n\nExample: `Your ID: $userID`\n\nOutput: `Your ID: 123456789`',
        '$mention': '**$mention** - Mention User\n\n📢 Creates clickable @mention.\n\nExample:\n```paracord\n$sendMessage("Hello $mention!")\n```\n\nOutput: `Hello @John!` (clickable)',
        '$userAvatar': '**$userAvatar** - Avatar URL\n\n🖼️ User\'s avatar image URL.\n\n**Uses:**\n- Embed thumbnails\n- Embed images\n\nExample:\n```paracord\n$thumbnail("$userAvatar")\n```',
        '$args': '**$args** - Command Arguments\n\n📝 All text after command.\n\nExample:\n```paracord\n$addCommand(\n  $name("say")\n  $sendMessage("$args")\n)\n```\n\nUsage: `!say Hello World`\nOutput: `Hello World`',
        '$value': '**$value** - Component Value\n\n🎛️ Value from button, select menu, or modal input.\n\n**Use in:**\n- Events (from button/select)\n- Conditionals\n- User variables\n\nExample:\n```paracord\n$if[$value==("yes")]\n  You clicked yes!\n$endif\n```',
        '$time': '**$time** - Cooldown Time\n\n⏰ Remaining cooldown time.\n\nOnly works in cooldown message.\n\nExample:\n```paracord\n$cooldown("1h;Come back in $time!")\n```\n\nOutput: `Come back in 45m 23s!`',
        '$timestamp': '**$timestamp** - Timestamp\n\n🕐 Current timestamp.\n\n**Use in:**\n- Embeds (shows current time)\n- User variables (store time)\n\nExample:\n```paracord\n$embed(\n  $timestamp\n)\n```',
        // Functions
        '$random': '**$random** - Random Number\n\n🎲 Generate random integer.\n\n**Syntax:** `$random(min,max)`\n\n**Supports:**\n- Positive: `$random(1,100)`\n- Negative: `$random(-100,-1)`\n- Mixed: `$random(-50,50)`\n\nExample:\n```paracord\n$sendMessage("You rolled $random(1,6)")\n$setUserVar($userID;coins;+$random(50,150))\n```',
        // Cooldowns
        '$cooldown': '**$cooldown** - Rate Limit\n\n⏱️ Add cooldown to command.\n\n**Syntax:** `$cooldown("duration;message")`\n\n**Duration:**\n- `30s` - 30 seconds\n- `5m` - 5 minutes\n- `1h` - 1 hour\n- `24h` - 24 hours\n\n**Variables in message:**\n- `$time` - Remaining time\n\nExample:\n```paracord\n$cooldown("24h;⏰ Wait $time!")\n```',
        // Conditionals
        '$if': '**$if** - Conditional Start\n\n🔀 Start conditional block.\n\n**Syntax:** `$if[condition]content$endif`\n\n**Operators:**\n- `==` - Equals\n- `!=` - Not equals\n- `>` - Greater than\n- `<` - Less than\n- `>=` - Greater or equal\n- `<=` - Less or equal\n\nExample:\n```paracord\n$if[$value==("yes")]\n  Yes chosen!\n$elseif[$value==("no")]\n  No chosen!\n$endif\n```',
        '$elseif': '**$elseif** - Else If\n\n🔀 Alternative condition.\n\n**Syntax:** `$elseif[condition]content`\n\nUse after `$if` for multiple conditions.\n\nExample:\n```paracord\n$if[$value==("a")]\n  A\n$elseif[$value==("b")]\n  B\n$elseif[$value==("c")]\n  C\n$endif\n```',
        '$else': '**$else** - Else\n\n🔀 Default case.\n\nRuns if no conditions match.\n\nExample:\n```paracord\n$if[$value==("yes")]\n  Yes\n$else\n  Not yes\n$endif\n```',
        '$endif': '**$endif** - End Conditional\n\n🔚 Close conditional block.\n\n**Required** after every `$if`!\n\nExample:\n```paracord\n$if[$value==("yes")]\n  Content\n$endif\n```',
        // Buttons
        '$newButton': '**$newButton** - Define Button\n\n🔘 Define reusable button.\n\n**Required:**\n- `$addButton` - Button properties\n- `$id` - Event ID\n\nExample:\n```paracord\n$newButton(\n  $addButton("btn_yes;Yes;success;yes;✅")\n  $id("handleChoice")\n)\n```',
        '$addButton': '**$addButton** - Button Properties\n\n🎨 Define button in compact format.\n\n**Syntax:** `$addButton("id;label;style;value;emoji")`\n\n**Styles:**\n- `primary` - Blue\n- `secondary` - Gray\n- `success` - Green\n- `danger` - Red\n\n**Parts:**\n- `id` - Button unique ID\n- `label` - Button text\n- `style` - Color\n- `value` - Value for conditionals (optional)\n- `emoji` - Emoji icon (optional)\n\nExample:\n```paracord\n$addButton("btn_yes;✅ Yes;success;yes;✅")\n```',
        '$useButton': '**$useButton** - Add Button\n\n➕ Add button to message.\n\n**Syntax:** `$useButton("button_id")`\n\n**Can use multiple times** (up to 5 per row, 25 total).\n\nExample:\n```paracord\n$useButton("btn_yes")\n$useButton("btn_no")\n$useButton("btn_maybe")\n```',
        '$id': '**$id** - Component ID\n\n🏷️ Unique identifier for component.\n\n**Use in:**\n- Buttons → Event ID\n- Select menus → Menu ID\n- Modals → Modal ID\n- Events → Handler ID\n\nExample:\n```paracord\n$id("handleClick")\n```\n\n💡 **Must match** event `$id`!',
        '$label': '**$label** - Button Label\n\n🔤 Text displayed on button.\n\nExample:\n```paracord\n$label("Click Me")\n```',
        '$style': '**$style** - Button Style\n\n🎨 Button color.\n\n**Options:**\n- `primary` - Blue (main actions)\n- `secondary` - Gray (neutral)\n- `success` - Green (confirm)\n- `danger` - Red (delete/cancel)\n\nExample:\n```paracord\n$style("success")\n```',
        '$emoji': '**$emoji** - Button Emoji\n\n😀 Emoji icon on button.\n\nExample:\n```paracord\n$emoji("👍")\n```',
        '$eventName': '**$eventName** - Link Event\n\n🔗 Event ID to trigger.\n\nMust match `$event($id("..."))`.\n\nExample:\n```paracord\n$eventName("handleClick")\n```',
        // Select Menus
        '$newSelectMenu': '**$newSelectMenu** - Define Select Menu\n\n📋 Define dropdown menu.\n\n**Required:**\n- `$id` - Menu ID\n- `$addSelectMenuOption` - Options\n\nExample:\n```paracord\n$newSelectMenu(\n  $id("select_role")\n  $placeholder("Choose role")\n  $addSelectMenuOption("opt1;Admin;admin")\n)\n```',
        '$addSelectMenuOption': '**$addSelectMenuOption** - Add Option\n\n➕ Add option to select menu.\n\n**Syntax:** `$addSelectMenuOption("id;label;value")`\n\n**Parts:**\n- `id` - Option ID\n- `label` - Display text\n- `value` - Value for conditionals\n\nExample:\n```paracord\n$addSelectMenuOption("opt1;Admin;admin")\n$addSelectMenuOption("opt2;Mod;mod")\n```',
        '$useSelectMenu': '**$useSelectMenu** - Add Select Menu\n\n➕ Add select menu to message.\n\n**Syntax:** `$useSelectMenu("menu_id")`\n\n⚠️ **Limit:** Only 1 per message (Discord limitation).\n\nExample:\n```paracord\n$useSelectMenu("select_role")\n```',
        '$placeholder': '**$placeholder** - Placeholder Text\n\n📝 Default text for select menu.\n\nExample:\n```paracord\n$placeholder("Choose an option...")\n```',
        // Modals
        '$newModal': '**$newModal** - Define Modal\n\n📝 Define modal form.\n\n**Required:**\n- `$id` - Modal ID\n- `$title` - Modal title\n- `$addTextInput` - Input fields\n\nExample:\n```paracord\n$newModal(\n  $id("modal_feedback")\n  $title("Feedback Form")\n  $addTextInput("input1;Name;2;50;Your name")\n)\n```',
        '$addTextInput': '**$addTextInput** - Add Input Field\n\n📝 Add text input to modal.\n\n**Syntax:** `$addTextInput("id;label;min;max;placeholder")`\n\n**Parts:**\n- `id` - Input ID\n- `label` - Field label\n- `min` - Min characters\n- `max` - Max characters\n- `placeholder` - Hint text (optional)\n\nExample:\n```paracord\n$addTextInput("input_msg;Message;10;500;Type here...")\n```',
        '$sendModal': '**$sendModal** - Send Modal\n\n📤 Send modal form.\n\n**Syntax:** `$sendModal("modal_id")`\n\n✅ **Can use in:**\n- Slash commands\n- Button events (v2.6+)\n\n❌ **Cannot use in:**\n- Text commands\n\nExample:\n```paracord\n$event(\n  $id("btn_feedback")\n  $sendModal("modal_feedback")\n)\n```',
        '$title': '**$title** - Title\n\n📌 Title text.\n\n**Use in:**\n- Modals → Form title\n- Embeds → Embed title\n\nExample:\n```paracord\n$title("Feedback Form")\n```',
        // Events
        '$event': '**$event** - Event Handler\n\n⚡ Handle button/select/modal events.\n\n**Required:**\n- `$id` - Event ID (must match component)\n- Response (`$sendMessage` or `$sendModal`)\n\nExample:\n```paracord\n$event(\n  $id("handleClick")\n  $sendMessage("Button clicked!")\n)\n```',
        // Embeds
        '$embed': '**$embed** - Rich Embed\n\n✨ Create rich embed message.\n\n**Required:**\n- `$embedName` - Reference name\n\n**Optional:**\n- `$title`, `$description`, `$color`\n- `$thumbnail`, `$image`\n- `$footer`, `$timestamp`\n- `$addField`\n\nExample:\n```paracord\n$embed(\n  $embedName("welcome")\n  $title("Welcome!")\n  $description("Hello $username")\n  $color("#5865F2")\n)\n```',
        '$embedName': '**$embedName** - Embed Name\n\n🏷️ Reference name for embed.\n\nUse in `$sendMessage("embedName")`.\n\nExample:\n```paracord\n$embedName("welcomeEmbed")\n```',
        '$color': '**$color** - Embed Color\n\n🎨 Border color in hex format.\n\n**Format:** `#RRGGBB`\n\n**Popular colors:**\n- `#5865F2` - Discord Blue\n- `#57F287` - Green\n- `#FEE75C` - Yellow\n- `#ED4245` - Red\n\nExample:\n```paracord\n$color("#5865F2")\n```',
        '$footer': '**$footer** - Embed Footer\n\n👣 Small text at bottom.\n\nExample:\n```paracord\n$footer("Paracord v2.8")\n```',
        '$thumbnail': '**$thumbnail** - Thumbnail Image\n\n🖼️ Small image (top right).\n\n**Syntax:** `$thumbnail("URL")`\n\n**Can use variables:**\n- `$userAvatar` - User\'s avatar\n\nExample:\n```paracord\n$thumbnail("$userAvatar")\n$thumbnail("https://example.com/logo.png")\n```',
        '$image': '**$image** - Large Image\n\n🖼️ Large image in embed body.\n\n**Syntax:** `$image("URL")`\n\nExample:\n```paracord\n$image("https://example.com/banner.png")\n```',
        '$addField': '**$addField** - Embed Field\n\n📋 Add field to embed.\n\n**Syntax:** `$addField("name;value;inline")`\n\n**Parts:**\n- `name` - Field title\n- `value` - Field content\n- `inline` - `true`/`false` (side-by-side)\n\n**Can add up to 25 fields.**\n\nExample:\n```paracord\n$addField("Balance;100 coins;true")\n$addField("Level;5;true")\n```'
    };
    return docs[word];
}
//# sourceMappingURL=extension.js.map