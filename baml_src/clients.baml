// Learn more about clients at https://docs.boundaryml.com/docs/snippets/clients/overview

client<llm> Llama32_11b_vision {
  provider openai-generic
  options {
    model "neuralmagic/Llama-3.2-11B-Vision-Instruct-FP8-dynamic"
    api_key "super-secret-key"
    base_url env.LLM_BASE_URL
    temperature 0.0
    seed 42
  }
}


client<llm> Gemini20Flash {
  provider vertex-ai
  options {
    model gemini-2.0-flash-001
    location us-central1
    generation_config {
      temperature 0.0
      seed 42
    }
  }
}

client<llm> CustomGPT4o {
  provider openai
  options {
    model "gpt-4o"
    api_key env.OPENAI_API_KEY
  }
}

client<llm> CustomGPT4oMini {
  provider openai
  retry_policy Exponential
  options {
    model "gpt-4o-mini"
    api_key env.OPENAI_API_KEY
  }
}

client<llm> CustomSonnet {
  provider anthropic
  options {
    model "claude-3-5-sonnet-20241022"
    api_key env.ANTHROPIC_API_KEY
    default_role "system"
  }
}


client<llm> CustomHaiku {
  provider anthropic
  retry_policy Constant
  options {
    model "claude-3-haiku-20240307"
    api_key env.ANTHROPIC_API_KEY
  }
}

client<llm> AppFallback {
  provider fallback
  retry_policy Exponential
  options {
    // This will try the clients in order until one succeeds
    strategy [Gemini20Flash, Llama32_11b_vision]
  }
}


// https://docs.boundaryml.com/docs/snippets/clients/round-robin
client<llm> CustomFast {
  provider round-robin
  options {
    // This will alternate between the two clients
    strategy [CustomGPT4oMini, CustomHaiku]
  }
}



// https://docs.boundaryml.com/docs/snippets/clients/retry
retry_policy Constant {
  max_retries 3
  // Strategy is optional
  strategy {
    type constant_delay
    delay_ms 200
  }
}

retry_policy Exponential {
  max_retries 2
  // Strategy is optional
  strategy {
    type exponential_backoff
    delay_ms 300
    multiplier 1.5
    max_delay_ms 10000
  }
}