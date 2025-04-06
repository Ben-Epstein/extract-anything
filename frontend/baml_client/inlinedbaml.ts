/*************************************************************************************************

Welcome to Baml! To use this generated code, please run one of the following:

$ npm install @boundaryml/baml
$ yarn add @boundaryml/baml
$ pnpm add @boundaryml/baml

*************************************************************************************************/

// This file was generated by BAML: do not edit it. Instead, edit the BAML
// files and re-generate this code.
//
/* eslint-disable */
// tslint:disable
// @ts-nocheck
// biome-ignore format: autogenerated code
const fileMap = {
  
  "clients.baml": "// Learn more about clients at https://docs.boundaryml.com/docs/snippets/clients/overview\n\nclient<llm> Llama32_11b_vision {\n  provider openai-generic\n  options {\n    model \"neuralmagic/Llama-3.2-11B-Vision-Instruct-FP8-dynamic\"\n    api_key \"super-secret-key\"\n    base_url env.LLM_BASE_URL\n    temperature 0.0\n    seed 42\n  }\n}\n\n\nclient<llm> Gemini20Flash {\n  provider vertex-ai\n  options {\n    model gemini-2.0-flash-001\n    location us-central1\n    credentials env.GOOGLE_APPLICATION_CREDENTIALS\n    generation_config {\n      temperature 0.0\n      seed 42\n    }\n  }\n}\n\nclient<llm> CustomGPT4o {\n  provider openai\n  options {\n    model \"gpt-4o\"\n    api_key env.OPENAI_API_KEY\n  }\n}\n\nclient<llm> CustomGPT4oMini {\n  provider openai\n  retry_policy Exponential\n  options {\n    model \"gpt-4o-mini\"\n    api_key env.OPENAI_API_KEY\n  }\n}\n\nclient<llm> CustomSonnet {\n  provider anthropic\n  options {\n    model \"claude-3-5-sonnet-20241022\"\n    api_key env.ANTHROPIC_API_KEY\n    default_role \"system\"\n  }\n}\n\n\nclient<llm> CustomHaiku {\n  provider anthropic\n  retry_policy Constant\n  options {\n    model \"claude-3-haiku-20240307\"\n    api_key env.ANTHROPIC_API_KEY\n  }\n}\n\nclient<llm> AppFallback {\n  provider fallback\n  retry_policy Exponential\n  options {\n    // This will try the clients in order until one succeeds\n    strategy [Gemini20Flash]//, Llama32_11b_vision]\n  }\n}\n\n\n// https://docs.boundaryml.com/docs/snippets/clients/round-robin\nclient<llm> CustomFast {\n  provider round-robin\n  options {\n    // This will alternate between the two clients\n    strategy [CustomGPT4oMini, CustomHaiku]\n  }\n}\n\n\n\n// https://docs.boundaryml.com/docs/snippets/clients/retry\nretry_policy Constant {\n  max_retries 3\n  // Strategy is optional\n  strategy {\n    type constant_delay\n    delay_ms 200\n  }\n}\n\nretry_policy Exponential {\n  max_retries 2\n  // Strategy is optional\n  strategy {\n    type exponential_backoff\n    delay_ms 300\n    multiplier 1.5\n    max_delay_ms 10000\n  }\n}",
  "execute_baml.baml": "// Defining a data model.\nclass Response {\n  @@dynamic\n}\n\nfunction ExecuteBAML(content: string | image | audio | image[]) -> Response {\n  client Gemini20Flash\n  prompt #\"\n    {{ _.role('user') }}\n\n    Extract the data from the given content.\n\n    {{ content }}\n\n    {{ ctx.output_format(prefix=\"Answer with this format:\\n\") }}\n    Your answer MUST be JSON! Wrap your answer in `\n  \"#\n}\n\n// Test the function with a sample resume. Open the VSCode playground to run this.\ntest vaibhav_resume {\n  functions [ExecuteBAML]\n  type_builder {\n    class Person {\n      name string @description(\"The full name of the individual\")\n      email string @description(\"The email address of the individual\")\n      experience Experience[]\n      skills string[]\n    }\n    \n    class Experience {\n      position string @description(\"The role held by the individual\")\n      company string @description(\"The company where the experience was gained\")\n    }\n\n    dynamic class Response {\n      result Person\n    }\n  }\n  args {\n    content #\"\n      Vaibhav Epstein\n      vbv@boundaryml.com\n\n      Experience:\n      - Founder at BoundaryML\n      - CV Engineer at Google\n      - CV Engineer at Microsoft\n\n      Skills:\n      - Rust\n      - C++\n    \"#\n  }\n}\n",
  "generate_baml.baml": "// Defining a data model.\nclass Schema {\n  interface_code string @description(#\"\n    You dont need escape characters.\n\n    Example:\n    class Schema {\n      name string\n      age int\n    }\n  \"#)\n  return_type string\n  other_code string\n}\n\nfunction GenerateBAML(content: string | image | audio | image[]) -> Schema @stream.not_null {\n  client Gemini20Flash\n  prompt #\"\n    {{ _.role('user') }}\n\n    Generate BAML schema for the given content.\n\n    {{ BAMLBackground() }}\n\n    {{ ctx.output_format(prefix=\"Answer with this format:\\n\") }}\n\n    {{ content }}\n  \"#\n}\n\n\ntemplate_string BAMLBackground() ##\"\n  BAML allows you to define schemas for your data.\n  Its almost like typescript, but with some differences.\n  - no colons for example\n\n  <Example Definition>\n    // Define output schemas using classes\n    class MyObject {\n      // Optional string fields use ?\n      // @description is optional, but if you include it, it goes after the field.\n      name string? @description(\"The name of the object\")\n      \n      // Arrays of primitives\n      // arrays cannot be optional.\n      tags string[]\n      \n      // Enums must be declared separately and are optional\n      status MyEnum?\n      \n      // Union types\n      type \"success\" | \"error\"\n      \n      // Primitive types\n      count int\n      enabled bool\n      score float\n\n      // nested objects\n      nested MyObject2\n    }\n\n    // Enums are declared separately\n    enum MyEnum {\n      PENDING\n      ACTIVE @description(\"Item is currently active\")\n      COMPLETE\n    }\n\n    // Type aliases\n    type Foo = string | int\n\n    // Recursive types\n    class Article {\n      title string\n      content string\n      sub_articles Article[]\n    }\n\n    // or with type alias\n    type JSON = string | int | float | boolean | null | JSON[] | map<string, JSON>\n\n    // Comments use double slashes\n    // inline class definitions are not supported\n  </Example Definition>\n\n  Do NOT use numbers as confidence intervals if you need to use them. Prefer an enum with descriptions or literals like \"high\", \"medium\", \"low\".\n\n  You must not use any of the following words as field names in your classes:\n    * class\n    * from\n    * type\n    * enum\n    * function\n    * test\n  If you need to use of one these, append an underscore like `type_` or `from_`\n  Every field must only contain 1 type\n\n  Dedent all declarations. You must include at least once class to define the final schema.\n\"##\n\n// Test the function with a sample resume. Open the VSCode playground to run this.\ntest vaibhav_resume {\n  functions [GenerateBAML]\n  args {\n    content #\"\n      Vaibhav Gupta\n      vbv@boundaryml.com\n\n      Experience:\n      - Founder at BoundaryML\n      - CV Engineer at Google\n      - CV Engineer at Microsoft\n\n      Skills:\n      - Rust\n      - C++\n    \"#\n  }\n}\n",
  "generators.baml": "// This helps use auto generate libraries you can use in the language of\n// your choice. You can have multiple generators if you use multiple languages.\n// Just ensure that the output_dir is different for each generator.\ngenerator py_target {\n    // Valid values: \"python/pydantic\", \"typescript\", \"ruby/sorbet\", \"rest/openapi\"\n    output_type \"python/pydantic\"\n\n    // Where the generated code will be saved (relative to baml_src/)\n    output_dir \"../src/shared\"\n\n    // The version of the BAML package you have installed (e.g. same version as your baml-py or @boundaryml/baml).\n    // The BAML VSCode extension version should also match this version.\n    version \"0.81.3\"\n\n    // Valid values: \"sync\", \"async\"\n    // This controls what `b.FunctionName()` will be (sync or async).\n    default_client_mode async\n}\n\ngenerator ts_target {\n    // Valid values: \"python/pydantic\", \"typescript\", \"ruby/sorbet\", \"rest/openapi\"\n    output_type \"typescript/react\"\n\n    // Where the generated code will be saved (relative to baml_src/)\n    output_dir \"../frontend\"\n\n    // The version of the BAML package you have installed (e.g. same version as your baml-py or @boundaryml/baml).\n    // The BAML VSCode extension version should also match this version.\n    version \"0.81.3\"\n\n    // Valid values: \"sync\", \"async\"\n    // This controls what `b.FunctionName()` will be (sync or async).\n    default_client_mode async\n}\n",
  "ndas.baml": "// Types don't support descriptions\ntype ValidDate = string @check(valid_date_format, {{ this|regex_match('^\\d{4}-\\d{2}-\\d{2}$')}})\n\nclass NDA {\n\n  title string\n  effective_date string @description(\"Formatted YYYY-MM-DD\") // Can't use ValidDate because fields with checks cannot be parameters to functions, and NDA is a param\n  agreement_type AgreementType\n  parties Party[]\n  confidential_information ConfidentialInformation\n  exclusions string[] @description(\"Information explicitly excluded from confidentiality obligations\")\n  obligations Obligation[]\n  term_duration Duration \n  confidentiality_period Duration\n  \n  governing_law string @description(\"The state or jurisdiction whose laws govern the agreement\")\n  dispute_resolution DisputeResolution\n  remedies Remedy[] @alias(\"breach_of_contract_remedies\") \n  \n  exhibits Exhibit[] @description(\"Additional attachments or exhibits to the agreement\")\n  signatures Signature[]\n}\n\nenum AgreementType {\n  MUTUAL\n  UNILATERAL\n}\nclass Party {\n  name string @description(\"Full legal name of the company or individual\")\n  type string @description(\"Type of entity (corporation, LLC, individual, etc.)\")\n  address Address\n  role PartyRole\n  contact_person ContactPerson? @alias(\"primary_contact_person\")\n}\n\nclass Address {\n  street string\n  city string\n  state string\n  zip string\n  country string?\n}\n\nenum PartyRole {\n  DISCLOSING_PARTY @description(\"Party sharing confidential information\")\n  RECEIVING_PARTY @description(\"Party receiving confidential information\")\n  BOTH @description(\"Party both shares and receives confidential information\")\n}\n\nclass ContactPerson {\n  name string\n  title string\n  email string\n  phone string?\n}\n\nclass ConfidentialInformation {\n  general_definition string @description(\"How confidential information is broadly defined\")\n  specific_items string[] @description(\"Specific items or categories explicitly mentioned as confidential\")\n}\n\nclass Obligation {\n  party_name string\n  descriptions string[] @description(\"Descriptions of what the party must or must not do\")\n}\n\nclass Duration {\n  length int\n  unit TimeUnit\n}\n\nenum TimeUnit {\n  DAYS\n  MONTHS\n  YEARS\n  INDEFINITE\n}\n\nclass DisputeResolution {\n  method string @description(\"Method of dispute resolution (litigation, arbitration, etc.)\")\n  location string\n}\nclass Remedy {\n  type string @description(\"Type of remedy (damages, injunctive relief, etc.)\")\n  description string\n}\nclass Exhibit {\n  title string\n  content string\n}\nclass Signature {\n  party_name string\n  signatory_name string\n  title string\n  date string @description(\"Date of signing. Formatted YYYY-MM-DD\") // We cant use checks because NDA is a function parameter. BAML doesnt support params with checks @check(valid_date_format, {{ this|regex_match('^\\\\d{4}-\\\\d{2}-\\\\d{2}$')}})\n}\n\nfunction ExtractNDA(document: string | image | image[]) -> NDA {\n  client AppFallback\n  prompt #\"\n    {{ _.role('user') }}\n\n    You are a legal AI assistant specializing in contract analysis. Please analyze the following Non-Disclosure Agreement (NDA) and extract the key information according to the specified format.\n\n    {{ document }}\n\n    {{ ctx.output_format(prefix=\"Please extract the following information in JSON format:\") }}\n  \"#\n}\n\nfunction AnalyzeNDARisks(nda: NDA) -> RiskAnalysis {\n  client AppFallback\n  prompt #\"\n    {{ _.role('system') }}\n    You are an expert legal AI specialized in analyzing legal risks in contracts.\n\n    {{ _.role('user') }}\n    Please analyze the following Non-Disclosure Agreement (NDA) for potential legal risks, ambiguities, or unfavorable terms. Provide a comprehensive risk assessment.\n\n    NDA Details:\n    Title: {{ nda.title }}\n    Type: {{ nda.agreement_type }}\n    Effective Date: {{ nda.effective_date }}\n\n    Parties:\n    {% for party in nda.parties %}\n    - {{ party.name }} ({{ party.role }})\n    {% endfor %}\n\n    Confidential Information:\n    {{ nda.confidential_information.general_definition }}\n    Specific items:\n    {% for item in nda.confidential_information.specific_items %}\n    - {{ item }}\n    {% endfor %}\n\n    Exclusions:\n    {% for exclusion in nda.exclusions %}\n    - {{ exclusion }}\n    {% endfor %}\n\n    Obligations:\n    {% for obligation in nda.obligations %}\n    {{ obligation.party_name }} must:\n    {% for desc in obligation.descriptions %}\n    - {{ desc }}\n    {% endfor %}\n    {% endfor %}\n\n    Term: {{ nda.term_duration.length }} {{ nda.term_duration.unit }}\n    Confidentiality Period: {{ nda.confidentiality_period.length }} {{ nda.confidentiality_period.unit }}\n    Governing Law: {{ nda.governing_law }}\n\n    {{ ctx.output_format(prefix=\"Please provide your risk analysis in the following format:\\n\") }}\n  \"#\n}\n\nenum RiskLevel {\n  LOW \n  MEDIUM\n  HIGH\n}\n\nclass RiskAnalysis {\n  overall_risk_level RiskLevel\n  key_risks Risk[]\n  recommendations string[]\n}\n\nclass Risk {\n  section string\n  description string\n  severity RiskLevel\n  potential_impact string\n}\n\n\nfunction TrackDeadlines(nda: NDA) -> DeadlineReport {\n  client AppFallback\n  prompt #\"\n    {{ _.role('user') }}\n    Based on the following NDA information, identify all key dates and deadlines that need to be tracked:\n\n    NDA Details:\n    Title: {{ nda.title }}\n    Effective Date: {{ nda.effective_date }}\n    Term Duration: {{ nda.term_duration.length }} {{ nda.term_duration.unit }}\n    Confidentiality Period: {{ nda.confidentiality_period.length }} {{ nda.confidentiality_period.unit }}\n\n    {{ ctx.output_format(prefix=\"Please identify all important dates and deadlines:\") }}\n  \"#\n}\n\nclass DeadlineReport {\n  expiration_date ValidDate @description(\"Formatted YYYY-MM-DD\")\n  confidentiality_end_date ValidDate @description(\"Formatted YYYY-MM-DD\")\n  key_milestones Milestone[] @description(\"Important milestones or deadlines\")\n}\n\nclass Milestone {\n  name string @description(\"Name of the milestone\")\n  date ValidDate @alias(\"milesone_date\") @description(\"Formatted YYYY-MM-DD\")\n  description string @description(\"Description of what happens on this date\")\n}\n\ntest sample_nda {\n  functions [ExtractNDA]\n  args {\n    document #\"\n      # MUTUAL NON-DISCLOSURE AGREEMENT\n\n      **THIS MUTUAL NON-DISCLOSURE AGREEMENT** (this \"Agreement\") is made and entered into as of June 15, 2025 (the \"Effective Date\"), by and between:\n\n      **TechInnovate Labs, Inc.**, a Delaware corporation, with its principal place of business at 1234 Innovation Way, San Francisco, CA 94105 (\"Company A\")\n\n      and\n\n      **GreenGrow Solutions, LLC**, a California limited liability company, with its principal place of business at 567 Sustainable Drive, Oakland, CA 94612 (\"Company B\").\n\n      [... rest of the agreement ...]\n    \"#\n  }\n}",
  "resume.baml": "// // Define output schemas using classes\n// class Person {\n//   name string @description(\"The name of the person\")\n//   experience Experience[]\n//   skills Skill[]\n// }\n\n// // class Name {\n// //   first string\n// //   last string\n// // }\n\n// class Experience {\n//   title string\n//   company string\n// }\n\n// class Skill {\n//   name string\n// }\n\n// function ExtractResume(resume_text: string) -> Person {\n//     client Gemini20Flash\n//     prompt #\"\n//         Extract the following resume:\n//         `\n//         {{ resume_text }}\n\n//         {{ ctx.output_format(prefix=\"Return your answer in the following format\") }}\n//     \"#\n// }\n\n",
}
export const getBamlFiles = () => {
    return fileMap;
}