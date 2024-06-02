#![allow(non_snake_case)]
use marine_rs_sdk::marine;
use marine_rs_sdk::module_manifest;
use reqwest::blocking::Client;
use serde::{Deserialize, Serialize};

module_manifest!();
pub fn main() {}
#[marine]
#[derive(Serialize, Deserialize)]
pub struct ProposalSummary {
    pub summary: String,
}

#[marine]
pub fn summarize_proposal(bytecode: String) -> ProposalSummary {
    let client = Client::new();
    let api_key = std::env::var("OPENAI_API_KEY").expect("OPENAI_API_KEY not set");
    let url = "https://api.openai.com/v1/chat/completions";

    let params = serde_json::json!({
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": "You are an AI that summarizes smart contract bytecode."},
            {"role": "user", "content": format!("Summarize the following smart contract bytecode: {}", bytecode)}
        ],
        "max_tokens": 150
    });

    let res = client
        .post(url)
        .header("Authorization", format!("Bearer {}", api_key))
        .json(&params)
        .send()
        .expect("Failed to call OpenAI API");

    let response_json: serde_json::Value = res.json().expect("Failed to parse response");
    let summary = response_json["choices"][0]["message"]["content"]
        .as_str()
        .unwrap()
        .to_string();

    ProposalSummary { summary }
}
