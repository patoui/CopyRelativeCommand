import sublime, sublime_plugin
from os.path import relpath
import json
import fnmatch

class CopyRelativeCommandCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        filename = self.view.file_name()
        if len(filename) > 0:
            shortest_relative_path = min(
                (
                    relpath(filename, folder)
                    for folder in sublime.active_window().folders()
                ),
                key=len,
            )

            language_settings = self.language_settings(self.get_language())

            if language_settings:
                for command in language_settings:
                    command_parts = command.get('command')
                    glob_pattern = command.get('glob', '*')

                    if fnmatch.fnmatch(shortest_relative_path, glob_pattern):
                        command = ''
                        for part in command_parts:
                            if '{' in part:
                                part = part.format(
                                    relative_path=shortest_relative_path,
                                    function=self.get_current_function())
                            command += ' ' + part

                        sublime.set_clipboard(command)
                        sublime.status_message("Copied relative command!")
                        return

            sublime.status_message("No relative commands to copy.")

    def is_enabled(self):
        return bool(self.view.file_name() and len(self.view.file_name()) > 0)

    def language_settings(self, name):
        languages = self.get_setting('languages')

        if languages:
            if name in languages:
                return languages[name]

        return None

    def get_language(self):
        symbol_regions = self.view.symbol_regions()

        if not symbol_regions:
            return ''

        # TODO: find better solution for determine language/source/syntax
        return symbol_regions[0].syntax.replace(' Source', '').lower()

    def get_setting(self, setting_name, default_value=None):
        settings = sublime.load_settings("CopyRelativeCommand.sublime-settings")
        return settings.get(setting_name, default_value)

    def get_current_function(self):
        selector = self.view.sel()[0]
        function_regions = self.view.find_by_selector('entity.name.function')
        current_function = None

        for region in reversed(function_regions):
            if region.a < selector.a:
                current_function = self.view.substr(region)
                break
        return current_function
