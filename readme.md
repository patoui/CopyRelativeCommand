# Copy Relative Command 📋️

A helpful command to copy a command to the clipboard based on configured settings, per language!

## Installation 💻️

Within Sublime Text:
- open the command palette (Windows/Linux: Ctrl + Shift + P, MacOS: Cmd + Shift + P)
- search for "Package Control: Install Package" and press enter
- search for "CopyRelativeCommand" and press enter on the mactching entry

### Alternative installation 💻️

Within terminal:
- clone this repository into your respective operating systems `Packages` directory
    - Linux: `cd ~/.config/sublime-text/Packages && git clone git@github.com:patoui/CopyRelativeCommand.git`
    - MacOS: `cd ~/Library/Application Support/Sublime Text 3/Packages && git clone git@github.com:patoui/CopyRelativeCommand.git`

## Quick start 🚀️

1. open command palette and search for "CopyRelativeCommand Settings"
2. add language settings, example:
```json
{
    "languages": {
        "php": [
            {
                "glob": "**Test.php",
                "command": [
                    "vendor/bin/phpunit",
                    "{relative_path}",
                    "--filter={current_function_or_class}"
                ]
            },
            {
                "glob": "*",
                "command": ["php -l {relative_path}"],
            },
        ],
    }
}
```
3. execute `CopyRelativeCommand` within the configured language, such as a `php` file in our above example:
    - if the open file (active view) is a file named `test/Unit/ExampleTest.php` and the cursor is within a function name `test_it_should_be_true`, the command copied to the clipboard would be:
        - `vendor/bin/phpunit test/Unit/ExampleTest.php --filter=test_it_should_be_true`
    - if the open file (active view) is a file named `app/Http/Controllers/UserController.php` the command copied to the clipboard would be:
        - `php -l app/Http/Controllers/UserController.php`
4. That's it! Add your own configurations for language commands 👌️

## Settings 👨‍💻️

<table>
    <thead>
        <tr>
            <th>Key</th>
            <th>Parent</th>
            <th>Description</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><code>languages</code></td>
            <td>N/A</td>
            <td>Contains a dictionary of all configured languages commands (e.g. <code>php</code>, <code>go</code>, <code>python</code>) and has a special value of <code>*<code> to apply to all languages</td>
        </tr>
        <tr>
            <td><code>glob<code></td>
            <td><code>languages.*</code></td>
            <td>contains a Unix filename pattern to identify which files the current command applies to (see <a href="https://docs.python.org/3/library/fnmatch.html">fnmatch</a> and <a href="https://en.wikipedia.org/wiki/Glob_(programming)) for more details">glob</a>)</td>
        </tr>
        <tr>
            <td><code>command</code></td>
            <td><code>languages.*</code></td>
            <td>
                a list (array) of strings which represent the command to be run. The <code>command</code> key has a few helper values:
                <ul>
                    <li><code>{relative_path}</code> will get the shortest relative path to the current file</li>
                    <li><code>{current_function}</code> will get the current function which the cursor is in, defaults to an empty string if it's unable to determine the current function</li>
                    <li><code>{current_function_or_class}</code> will get the current function which the cursor is in, if it's not available, it will fallback to the current class, if that's not available it defaults to an empty string</li>
                </ul>
            </td>
        </tr>
    </tbody>
</table>
