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
import type { BamlRuntime, BamlCtxManager, ClientRegistry, Image, Audio, Collector } from "@boundaryml/baml"
import { toBamlError } from "@boundaryml/baml"
import type { Checked, Check } from "./types"
import type { partial_types } from "./partial_types"
import type * as types from "./types"
import type {Address, AgreementType, ConfidentialInformation, ContactPerson, DeadlineReport, DisputeResolution, Duration, Exhibit, Milestone, NDA, Obligation, Party, PartyRole, Remedy, Response, Risk, RiskAnalysis, RiskLevel, Schema, Signature, TimeUnit} from "./types"
import type TypeBuilder from "./type_builder"

export class LlmResponseParser {
  constructor(private runtime: BamlRuntime, private ctxManager: BamlCtxManager) {}

  
  AnalyzeNDARisks(
      llmResponse: string,
      __baml_options__?: { tb?: TypeBuilder, clientRegistry?: ClientRegistry }
  ): RiskAnalysis {
    try {
      return this.runtime.parseLlmResponse(
        "AnalyzeNDARisks",
        llmResponse,
        false,
        this.ctxManager.cloneContext(),
        __baml_options__?.tb?.__tb(),
        __baml_options__?.clientRegistry,
      ) as RiskAnalysis
    } catch (error) {
      throw toBamlError(error);
    }
  }
  
  ExecuteBAML(
      llmResponse: string,
      __baml_options__?: { tb?: TypeBuilder, clientRegistry?: ClientRegistry }
  ): Response {
    try {
      return this.runtime.parseLlmResponse(
        "ExecuteBAML",
        llmResponse,
        false,
        this.ctxManager.cloneContext(),
        __baml_options__?.tb?.__tb(),
        __baml_options__?.clientRegistry,
      ) as Response
    } catch (error) {
      throw toBamlError(error);
    }
  }
  
  ExtractNDA(
      llmResponse: string,
      __baml_options__?: { tb?: TypeBuilder, clientRegistry?: ClientRegistry }
  ): NDA {
    try {
      return this.runtime.parseLlmResponse(
        "ExtractNDA",
        llmResponse,
        false,
        this.ctxManager.cloneContext(),
        __baml_options__?.tb?.__tb(),
        __baml_options__?.clientRegistry,
      ) as NDA
    } catch (error) {
      throw toBamlError(error);
    }
  }
  
  GenerateBAML(
      llmResponse: string,
      __baml_options__?: { tb?: TypeBuilder, clientRegistry?: ClientRegistry }
  ): Schema {
    try {
      return this.runtime.parseLlmResponse(
        "GenerateBAML",
        llmResponse,
        false,
        this.ctxManager.cloneContext(),
        __baml_options__?.tb?.__tb(),
        __baml_options__?.clientRegistry,
      ) as Schema
    } catch (error) {
      throw toBamlError(error);
    }
  }
  
  TrackDeadlines(
      llmResponse: string,
      __baml_options__?: { tb?: TypeBuilder, clientRegistry?: ClientRegistry }
  ): DeadlineReport {
    try {
      return this.runtime.parseLlmResponse(
        "TrackDeadlines",
        llmResponse,
        false,
        this.ctxManager.cloneContext(),
        __baml_options__?.tb?.__tb(),
        __baml_options__?.clientRegistry,
      ) as DeadlineReport
    } catch (error) {
      throw toBamlError(error);
    }
  }
  
}

export class LlmStreamParser {
  constructor(private runtime: BamlRuntime, private ctxManager: BamlCtxManager) {}

  
  AnalyzeNDARisks(
      llmResponse: string,
      __baml_options__?: { tb?: TypeBuilder, clientRegistry?: ClientRegistry }
  ): partial_types.RiskAnalysis {
    try {
      return this.runtime.parseLlmResponse(
        "AnalyzeNDARisks",
        llmResponse,
        true,
        this.ctxManager.cloneContext(),
        __baml_options__?.tb?.__tb(),
        __baml_options__?.clientRegistry,
      ) as partial_types.RiskAnalysis
    } catch (error) {
      throw toBamlError(error);
    }
  }
  
  ExecuteBAML(
      llmResponse: string,
      __baml_options__?: { tb?: TypeBuilder, clientRegistry?: ClientRegistry }
  ): partial_types.Response {
    try {
      return this.runtime.parseLlmResponse(
        "ExecuteBAML",
        llmResponse,
        true,
        this.ctxManager.cloneContext(),
        __baml_options__?.tb?.__tb(),
        __baml_options__?.clientRegistry,
      ) as partial_types.Response
    } catch (error) {
      throw toBamlError(error);
    }
  }
  
  ExtractNDA(
      llmResponse: string,
      __baml_options__?: { tb?: TypeBuilder, clientRegistry?: ClientRegistry }
  ): partial_types.NDA {
    try {
      return this.runtime.parseLlmResponse(
        "ExtractNDA",
        llmResponse,
        true,
        this.ctxManager.cloneContext(),
        __baml_options__?.tb?.__tb(),
        __baml_options__?.clientRegistry,
      ) as partial_types.NDA
    } catch (error) {
      throw toBamlError(error);
    }
  }
  
  GenerateBAML(
      llmResponse: string,
      __baml_options__?: { tb?: TypeBuilder, clientRegistry?: ClientRegistry }
  ): partial_types.Schema {
    try {
      return this.runtime.parseLlmResponse(
        "GenerateBAML",
        llmResponse,
        true,
        this.ctxManager.cloneContext(),
        __baml_options__?.tb?.__tb(),
        __baml_options__?.clientRegistry,
      ) as partial_types.Schema
    } catch (error) {
      throw toBamlError(error);
    }
  }
  
  TrackDeadlines(
      llmResponse: string,
      __baml_options__?: { tb?: TypeBuilder, clientRegistry?: ClientRegistry }
  ): partial_types.DeadlineReport {
    try {
      return this.runtime.parseLlmResponse(
        "TrackDeadlines",
        llmResponse,
        true,
        this.ctxManager.cloneContext(),
        __baml_options__?.tb?.__tb(),
        __baml_options__?.clientRegistry,
      ) as partial_types.DeadlineReport
    } catch (error) {
      throw toBamlError(error);
    }
  }
  
}