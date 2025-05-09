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
import type { Image, Audio } from "@boundaryml/baml"
import type { Checked, Check } from "./types"
import type {  Address,  AgreementType,  ConfidentialInformation,  ContactPerson,  DeadlineReport,  DisputeResolution,  Duration,  Exhibit,  Milestone,  NDA,  Obligation,  Party,  PartyRole,  Remedy,  Response,  Risk,  RiskAnalysis,  RiskLevel,  Schema,  Signature,  TimeUnit } from "./types"
import type * as types from "./types"

/******************************************************************************
*
*  These types are used for streaming, for when an instance of a type
*  is still being built up and any of its fields is not yet fully available.
*
******************************************************************************/

export interface StreamState<T> {
    value: T
    state: "Pending" | "Incomplete" | "Complete"
}

export namespace partial_types {
    
    export interface Address {
        street?: (string | null)
        city?: (string | null)
        state?: (string | null)
        zip?: (string | null)
        country: ((string | null) | null)
    }
    
    export interface ConfidentialInformation {
        general_definition?: (string | null)
        specific_items?: (string | null)[]
    }
    
    export interface ContactPerson {
        name?: (string | null)
        title?: (string | null)
        email?: (string | null)
        phone: ((string | null) | null)
    }
    
    export interface DeadlineReport {
        expiration_date?: Checked<(string | null),"valid_date_format">
        confidentiality_end_date?: Checked<(string | null),"valid_date_format">
        key_milestones?: (partial_types.Milestone | null)[]
    }
    
    export interface DisputeResolution {
        method?: (string | null)
        location?: (string | null)
    }
    
    export interface Duration {
        length?: (number | null)
        unit?: (TimeUnit | null)
    }
    
    export interface Exhibit {
        title?: (string | null)
        content?: (string | null)
    }
    
    export interface Milestone {
        name?: (string | null)
        date?: Checked<(string | null),"valid_date_format">
        description?: (string | null)
    }
    
    export interface NDA {
        title?: (string | null)
        effective_date?: (string | null)
        agreement_type?: (AgreementType | null)
        parties?: (partial_types.Party | null)[]
        confidential_information?: (partial_types.ConfidentialInformation | null)
        exclusions?: (string | null)[]
        obligations?: (partial_types.Obligation | null)[]
        term_duration?: (partial_types.Duration | null)
        confidentiality_period?: (partial_types.Duration | null)
        governing_law?: (string | null)
        dispute_resolution?: (partial_types.DisputeResolution | null)
        remedies?: (partial_types.Remedy | null)[]
        exhibits?: (partial_types.Exhibit | null)[]
        signatures?: (partial_types.Signature | null)[]
    }
    
    export interface Obligation {
        party_name?: (string | null)
        descriptions?: (string | null)[]
    }
    
    export interface Party {
        name?: (string | null)
        type?: (string | null)
        address?: (partial_types.Address | null)
        role?: (PartyRole | null)
        contact_person: ((partial_types.ContactPerson | null) | null)
    }
    
    export interface Remedy {
        type?: (string | null)
        description?: (string | null)
    }
    
    export interface Response {
        [key: string]: any;
    }
    
    export interface Risk {
        section?: (string | null)
        description?: (string | null)
        severity?: (RiskLevel | null)
        potential_impact?: (string | null)
    }
    
    export interface RiskAnalysis {
        overall_risk_level?: (RiskLevel | null)
        key_risks?: (partial_types.Risk | null)[]
        recommendations?: (string | null)[]
    }
    
    export interface Schema {
        interface_code?: (string | null)
        return_type?: (string | null)
        other_code?: (string | null)
    }
    
    export interface Signature {
        party_name?: (string | null)
        signatory_name?: (string | null)
        title?: (string | null)
        date?: (string | null)
    }
    
}