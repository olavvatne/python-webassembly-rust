wit_bindgen_guest_rust::export!("wits/markdown.wit");
use pulldown_cmark::{html, Parser};

struct Markdown;

impl markdown::Markdown for Markdown {
    fn render(input: String) -> String {
        let parser = Parser::new(&input);
        let mut html_output = String::new();
        html::push_html(&mut html_output, parser);
        return html_output;
    }

    fn overhead(input: String) -> (String, u64) {
        let s = std::time::Instant::now();
        let parser = Parser::new(&input);
        let mut html_output = String::new();
        html::push_html(&mut html_output, parser);
        let ms = s.elapsed().as_nanos();

        (html_output, ms as u64)
    }
}