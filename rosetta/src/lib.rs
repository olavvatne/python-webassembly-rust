wit_bindgen_rust::export!("wits/rosetta.wit");

struct Rosetta;

impl rosetta::Rosetta for Rosetta {
    fn occurrences(text: String, matching: String) -> u32 {
        return text.matches(&matching).count() as u32
    }
}