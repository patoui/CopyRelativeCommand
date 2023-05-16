import sublime, sublime_plugin
from os.path import relpath
import json
import fnmatch

class CopyRelativeCommandCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        filename = self.view.file_name()
        if len(filename) > 0:
            relative_path = min(
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

                    if fnmatch.fnmatch(relative_path, glob_pattern):
                        command = ''
                        for part in command_parts:
                            if '{' in part:
                                part = part.format(
                                    relative_path=relative_path,
                                    current_function=self.get_current_function(),
                                    current_class=self.get_current_class(),
                                    current_function_or_class=self.get_current_function_or_class())
                            command += part + ' '

                        sublime.set_clipboard(command.rstrip())
                        sublime.status_message("Copied relative command!")
                        return

            sublime.status_message("No relative commands to copy.")

    def is_enabled(self):
        return bool(self.view.file_name() and len(self.view.file_name()) > 0)

    def language_settings(self, name):
        languages = self.get_setting('languages')

        if not languages or name not in languages:
            return None

        return languages[name]

    def get_language(self):
        syntax = self.view.syntax()

        if not syntax:
            return ''

        return syntax.name.lower()

    def get_setting(self, setting_name, default_value=None):
        settings = sublime.load_settings("CopyRelativeCommand.sublime-settings")
        return settings.get(setting_name, default_value)

    def get_current_function_or_class(self):
        current_function = self.get_current_function()

        if len(current_function) > 0:
            return current_function

        return self.get_current_class()

    def get_current_class(self):
        return self.get_current_scope('entity.name.class')

    def get_current_function(self):
        return self.get_current_scope('entity.name.function')

    def get_current_scope(self, scope):
        selector = self.view.sel()[0]
        scope_regions = self.view.find_by_selector(scope)
        current_scope = ''

        for region in reversed(scope_regions):
            if region.a < selector.a:
                current_scope = self.view.substr(region)
                break

        return current_scope
