type ValidDate = string @check(valid_date_format, {{ this|regex_match('^\d{4}-\d{2}-\d{2}$')}})

class NDA {
  // Basic contract information
  title string
  effective_date string @description("The date when the agreement becomes effective")
  agreement_type AgreementType @description("Whether the NDA is unilateral or mutual")
  
  // Parties involved
  parties Party[] @description("The organizations or individuals involved in the agreement")
  
  // Core NDA content
  confidential_information ConfidentialInformation @description("Definition and scope of what is considered confidential")
  exclusions string[] @description("Information explicitly excluded from confidentiality obligations")
  obligations Obligation[] @description("Responsibilities of the receiving parties")
  
  // Time-related information
  term_duration Duration @description("How long the agreement will last")
  confidentiality_period Duration @description("How long confidentiality must be maintained")
  
  // Legal provisions
  governing_law string @description("The state or jurisdiction whose laws govern the agreement")
  dispute_resolution DisputeResolution @description("How disputes will be handled")
  remedies Remedy[] @description("Available remedies for breach of contract")
  
  // Additional information
  exhibits Exhibit[] @description("Additional attachments or exhibits to the agreement")
  signatures Signature[] @description("Signatures of the parties")
}

// Types of NDAs
enum AgreementType {
  MUTUAL @description("Both parties disclose confidential information to each other")
  UNILATERAL @description("Only one party discloses confidential information")
}

// Parties to the agreement
class Party {
  name string @description("Full legal name of the company or individual")
  type string @description("Type of entity (corporation, LLC, individual, etc.)")
  address Address @description("Physical address of the party")
  role PartyRole @description("Role in the agreement")
  contact_person ContactPerson? @description("Primary contact for the party")
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

// Confidential information details
class ConfidentialInformation {
  general_definition string @description("How confidential information is broadly defined")
  specific_items string[] @description("Specific items or categories explicitly mentioned as confidential")
}

// Obligations of the parties
class Obligation {
  party_name string @description("Name of the party with this obligation")
  descriptions string[] @description("Descriptions of what the party must or must not do")
}

// Time periods
class Duration {
  length int @description("Numeric length of time")
  unit TimeUnit @description("Unit of time measurement")
}

enum TimeUnit {
  DAYS
  MONTHS
  YEARS
  INDEFINITE
}

// Dispute resolution information
class DisputeResolution {
  method string @description("Method of dispute resolution (litigation, arbitration, etc.)")
  location string @description("Location where disputes will be resolved")
}

// Available remedies
class Remedy {
  type string @description("Type of remedy (damages, injunctive relief, etc.)")
  description string @description("Description of the remedy")
}

// Exhibits or attachments
class Exhibit {
  title string
  content string @description("Content or summary of the exhibit")
}

// Signature information
class Signature {
  party_name string
  signatory_name string @description("Name of the person signing")
  title string @description("Title of the signatory")
  date string @description("Date of signing. Formatted YYYY-MM-DD") // We cant use checks because NDA is a function parameter. BAML doesnt support params with checks @check(valid_date_format, {{ this|regex_match('^\\d{4}-\\d{2}-\\d{2}$')}})
}

// Main extraction function
function ExtractNDA(document: string | image | image[]) -> NDA {
  client AppFallback
  prompt #"
    {{ _.role('user') }}

    You are a legal AI assistant specializing in contract analysis. Please analyze the following Non-Disclosure Agreement (NDA) and extract the key information according to the specified format.

    {{ document }}

    {{ ctx.output_format(prefix="Please extract the following information in JSON format:") }}
  "#
}

// Risk analysis function
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

    {{ ctx.output_format(prefix="Please provide your risk analysis:") }}
  "#
}

// Risk analysis output schema
class RiskAnalysis {
  overall_risk_level RiskLevel @description("Overall risk assessment of the NDA")
  key_risks Risk[] @description("List of identified risks")
  recommendations string[] @description("Recommendations to mitigate risks")
}

enum RiskLevel {
  LOW @description("Minimal risk, standard terms")
  MEDIUM @description("Some concerning terms that warrant attention")
  HIGH @description("Significant risks that require negotiation")
}

class Risk {
  section string @description("Section of the NDA where the risk is found")
  description string @description("Description of the risk")
  severity RiskSeverity @description("How severe the risk is")
  potential_impact string @description("Potential impact of the risk")
}

enum RiskSeverity {
  LOW
  MEDIUM
  HIGH
}

// Deadline tracking function
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
  effective_date ValidDate @description("When the agreement becomes effective. Formatted YYYY-MM-DD")
  expiration_date ValidDate @description("When the agreement expires. Formatted YYYY-MM-DD")
  confidentiality_end_date ValidDate @description("When confidentiality obligations end. Formatted YYYY-MM-DD")
  key_milestones Milestone[] @description("Important milestones or deadlines")
}

class Milestone {
  name string @description("Name of the milestone")
  date ValidDate @description("Date of the milestone. Formatted YYYY-MM-DD")
  description string @description("Description of what happens on this date")
}

// Test functions with sample data
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