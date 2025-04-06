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
import type { Check, Checked  } from "../types";
import type { Image, Audio } from "@boundaryml/baml";

import type {  Address,  AgreementType,  ConfidentialInformation,  ContactPerson,  DeadlineReport,  DisputeResolution,  Duration,  Exhibit,  Milestone,  NDA,  Obligation,  Party,  PartyRole,  Remedy,  Response,  Risk,  RiskAnalysis,  RiskLevel,  Schema,  Signature,  TimeUnit } from "../types"

import type * as types from "../types"
import type { partial_types }from "../partial_types";

export type StreamingServerTypes = {
  AnalyzeNDARisks: partial_types.RiskAnalysis,
  ExecuteBAML: partial_types.Response,
  ExtractNDA: partial_types.NDA,
  GenerateBAML: partial_types.Schema,
  TrackDeadlines: partial_types.DeadlineReport,
}