// Types don't support descriptions
type ValidDate = string @check(valid_date_format, {{ this|regex_match('^\d{4}-\d{2}-\d{2}$')}})

class NDA {

  title string
  effective_date string @description("Formatted YYYY-MM-DD") // Can't use ValidDate because fields with checks cannot be parameters to functions, and NDA is a param
  agreement_type AgreementType
  parties Party[]
  confidential_information ConfidentialInformation
  exclusions string[] @description("Information explicitly excluded from confidentiality obligations")
  obligations Obligation[]
  term_duration Duration 
  confidentiality_period Duration
  
  governing_law string @description("The state or jurisdiction whose laws govern the agreement")
  dispute_resolution DisputeResolution
  remedies Remedy[] @alias("breach_of_contract_remedies") 
  
  exhibits Exhibit[] @description("Additional attachments or exhibits to the agreement")
  signatures Signature[]
}

enum AgreementType {
  MUTUAL
  UNILATERAL
}
class Party {
  name string @description("Full legal name of the company or individual")
  type string @description("Type of entity (corporation, LLC, individual, etc.)")
  address Address
  role PartyRole
  contact_person ContactPerson? @alias("primary_contact_person")
}

class Address {
  street string
  city string
  state string
  zip string
  country string?
}

enum PartyRole {
  DISCLOSING_PARTY @description("Party sharing confidential information")
  RECEIVING_PARTY @description("Party receiving confidential information")
  BOTH @description("Party both shares and receives confidential information")
}

class ContactPerson {
  name string
  title string
  email string
  phone string?
}

class ConfidentialInformation {
  general_definition string @description("How confidential information is broadly defined")
  specific_items string[] @description("Specific items or categories explicitly mentioned as confidential")
}

class Obligation {
  party_name string
  descriptions string[] @description("Descriptions of what the party must or must not do")
}

class Duration {
  length int
  unit TimeUnit
}

enum TimeUnit {
  DAYS
  MONTHS
  YEARS
  INDEFINITE
}

class DisputeResolution {
  method string @description("Method of dispute resolution (litigation, arbitration, etc.)")
  location string
}
class Remedy {
  type string @description("Type of remedy (damages, injunctive relief, etc.)")
  description string
}
class Exhibit {
  title string
  content string
}
class Signature {
  party_name string
  signatory_name string
  title string
  date string @description("Date of signing. Formatted YYYY-MM-DD") // We cant use checks because NDA is a function parameter. BAML doesnt support params with checks @check(valid_date_format, {{ this|regex_match('^\\d{4}-\\d{2}-\\d{2}$')}})
}

function ExtractNDA(document: string | image | image[]) -> NDA {
  client AppFallback
  prompt #"
    {{ _.role('user') }}

    You are a legal AI assistant specializing in contract analysis. Please analyze the following Non-Disclosure Agreement (NDA) and extract the key information according to the specified format.

    {{ document }}

    {{ ctx.output_format(prefix="Please extract the following information in JSON format:") }}
  "#
}

function AnalyzeNDARisks(nda: NDA) -> RiskAnalysis {
  client AppFallback
  prompt #"
    {{ _.role('system') }}
    You are an expert legal AI specialized in analyzing legal risks in contracts.

    {{ _.role('user') }}
    Please analyze the following Non-Disclosure Agreement (NDA) for potential legal risks, ambiguities, or unfavorable terms. Provide a comprehensive risk assessment.

    NDA Details:
    Title: {{ nda.title }}
    Type: {{ nda.agreement_type }}
    Effective Date: {{ nda.effective_date }}

    Parties:
    {% for party in nda.parties %}
    - {{ party.name }} ({{ party.role }})
    {% endfor %}

    Confidential Information:
    {{ nda.confidential_information.general_definition }}
    Specific items:
    {% for item in nda.confidential_information.specific_items %}
    - {{ item }}
    {% endfor %}

    Exclusions:
    {% for exclusion in nda.exclusions %}
    - {{ exclusion }}
    {% endfor %}

    Obligations:
    {% for obligation in nda.obligations %}
    {{ obligation.party_name }} must:
    {% for desc in obligation.descriptions %}
    - {{ desc }}
    {% endfor %}
    {% endfor %}

    Term: {{ nda.term_duration.length }} {{ nda.term_duration.unit }}
    Confidentiality Period: {{ nda.confidentiality_period.length }} {{ nda.confidentiality_period.unit }}
    Governing Law: {{ nda.governing_law }}

    {{ ctx.output_format(prefix="Please provide your risk analysis in the following format:\n") }}
  "#
}

enum RiskLevel {
  LOW 
  MEDIUM
  HIGH
}

class RiskAnalysis {
  overall_risk_level RiskLevel
  key_risks Risk[]
  recommendations string[]
}

class Risk {
  section string
  description string
  severity RiskLevel
  potential_impact string
}


function TrackDeadlines(nda: NDA) -> DeadlineReport {
  client AppFallback
  prompt #"
    {{ _.role('user') }}
    Based on the following NDA information, identify all key dates and deadlines that need to be tracked:

    NDA Details:
    Title: {{ nda.title }}
    Effective Date: {{ nda.effective_date }}
    Term Duration: {{ nda.term_duration.length }} {{ nda.term_duration.unit }}
    Confidentiality Period: {{ nda.confidentiality_period.length }} {{ nda.confidentiality_period.unit }}

    {{ ctx.output_format(prefix="Please identify all important dates and deadlines:") }}
  "#
}

class DeadlineReport {
  expiration_date ValidDate @description("Formatted YYYY-MM-DD")
  confidentiality_end_date ValidDate @description("Formatted YYYY-MM-DD")
  key_milestones Milestone[] @description("Important milestones or deadlines")
}

class Milestone {
  name string @description("Name of the milestone")
  date ValidDate @alias("milesone_date") @description("Formatted YYYY-MM-DD")
  description string @description("Description of what happens on this date")
}

test sample_nda {
  functions [ExtractNDA]
  args {
    document #"
      # MUTUAL NON-DISCLOSURE AGREEMENT

      **THIS MUTUAL NON-DISCLOSURE AGREEMENT** (this "Agreement") is made and entered into as of June 15, 2025 (the "Effective Date"), by and between:

      **TechInnovate Labs, Inc.**, a Delaware corporation, with its principal place of business at 1234 Innovation Way, San Francisco, CA 94105 ("Company A")

      and

      **GreenGrow Solutions, LLC**, a California limited liability company, with its principal place of business at 567 Sustainable Drive, Oakland, CA 94612 ("Company B").

      [... rest of the agreement ...]
    "#
  }
}