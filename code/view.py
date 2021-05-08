#-----------------------------------------------------------------------------
# This class loads html files from the "template" directory and formats them using Python.
# You can find a fuller explanation for this file in the README file
#-----------------------------------------------------------------------------

from bottle import SimpleTemplate
import string

class View():
    '''
        A general purpose view generator
        Takes template files and dictionaries and formats them
        
        Has default header/tailer behaviour

        To display different headers when logged in, be sure to replace the
        header keyword argument when calling the function from model
    '''
    def __init__(self, 
        template_path="templates/",  # Path to template files
        template_extension=".html",  # Extension of templates, self can be overridden
        **kwargs): # Used to pass any global format arguments
        self.template_path = template_path
        self.template_extension = template_extension
        self.global_renders = kwargs


    def __call__(self, *args, **kwargs):
        '''
            Call defaults to load and render
        '''
        return self.load_and_render(*args, **kwargs)


    def load_and_render(self, filename, header="header", tailer="tailer", **kwargs):
        ''' 
            Loads and renders templates

            :: filename :: Name of the template to load
            :: header :: Header template to use, swap this out for multiple headers 
            :: tailer :: Tailer template to use
            :: kwargs :: Keyword arguments to pass
        '''
        body_tpl = self.load_template(filename)
        header_tpl= self.load_template(header)
        tailer_tpl= self.load_template(tailer)

        rendered_template = self.render(
            body_template=body_tpl, 
            header_template=header_tpl, 
            tailer_template=tailer_tpl, 
            **kwargs)

        return rendered_template


    def load_template(self, filename):
        '''
            simple_render 
            A simple render using the format method
            
            :: template :: The template to use
            :: kwargs :: A dictionary of key value pairs to pass to the template
        '''
        path = self.template_path + filename + self.template_extension
        file = open(path, 'r')
        text = ""
        for line in file:
            text+= line
        file.close()
        tpl = SimpleTemplate(text)
        return tpl


    def render(self, body_template, header_template, tailer_template, **kwargs):
        ''' 
            render
            A more complex render that joins global settings with local settings

            :: template :: The template to use
            :: kwargs :: The local key value pairs to pass to the template
        '''
        # Construct the head, body and tail separately 
        # global renders will be overidden by k,v from kwargs
        rendered_body = body_template.render(self.global_renders | kwargs)
        rendered_head = header_template.render(self.global_renders | kwargs)
        rendered_tail = tailer_template.render(self.global_renders | kwargs)

        # Join them
        rendered_template = rendered_head + rendered_body + rendered_tail

        # Return the template
        return rendered_template


    def simple_render(self, template, **kwargs):
        '''
            simple_render 
            A simple render using the format method
            
            :: template :: The template to use
            :: kwargs :: A dictionary of key value pairs to pass to the template
        '''
        template = string.Template(template)
        template = template.safe_substitute(**kwargs)
        return  template


    def global_render(self, template):
        '''
            global_render 
            Renders using the global defaults
            
            :: template :: The template to use
        '''
        return self.simple_render(template, **self.global_renders)
