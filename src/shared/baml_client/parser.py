###############################################################################
#
#  Welcome to Baml! To use this generated code, please run the following:
#
#  $ pip install baml-py
#
###############################################################################

# This file was generated by BAML: please do not edit it. Instead, edit the
# BAML files and re-generate this code.
#
# ruff: noqa: E501,F401,F821
# flake8: noqa: E501,F401,F821
# pylint: disable=unused-import,line-too-long
# fmt: off
from typing import Any, Dict, List, Literal, Optional, Type, TypedDict, Union, cast

import baml_py
from typing_extensions import NotRequired

from . import partial_types, types
from .type_builder import TypeBuilder
from .types import Check, Checked


class BamlCallOptions(TypedDict, total=False):
    tb: NotRequired[TypeBuilder]
    client_registry: NotRequired[baml_py.baml_py.ClientRegistry]


class LlmResponseParser:
    __runtime: baml_py.BamlRuntime
    __ctx_manager: baml_py.BamlCtxManager

    def __init__(self, runtime: baml_py.BamlRuntime, ctx_manager: baml_py.BamlCtxManager):
      self.__runtime = runtime
      self.__ctx_manager = ctx_manager


    def AnalyzeNDARisks(
        self,
        llm_response: str,
        baml_options: BamlCallOptions = {},
    ) -> types.RiskAnalysis:
      __tb__ = baml_options.get("tb", None)
      if __tb__ is not None:
        tb = __tb__._tb # type: ignore (we know how to use this private attribute)
      else:
        tb = None
      __cr__ = baml_options.get("client_registry", None)

      parsed = self.__runtime.parse_llm_response(
        "AnalyzeNDARisks",
        llm_response,
        types,
        types,
        partial_types,
        False,
        self.__ctx_manager.get(),
        tb,
        __cr__,
      )

      return cast(types.RiskAnalysis, parsed)

    def ExecuteBAML(
        self,
        llm_response: str,
        baml_options: BamlCallOptions = {},
    ) -> types.Response:
      __tb__ = baml_options.get("tb", None)
      if __tb__ is not None:
        tb = __tb__._tb # type: ignore (we know how to use this private attribute)
      else:
        tb = None
      __cr__ = baml_options.get("client_registry", None)

      parsed = self.__runtime.parse_llm_response(
        "ExecuteBAML",
        llm_response,
        types,
        types,
        partial_types,
        False,
        self.__ctx_manager.get(),
        tb,
        __cr__,
      )

      return cast(types.Response, parsed)

    def ExtractNDA(
        self,
        llm_response: str,
        baml_options: BamlCallOptions = {},
    ) -> types.NDA:
      __tb__ = baml_options.get("tb", None)
      if __tb__ is not None:
        tb = __tb__._tb # type: ignore (we know how to use this private attribute)
      else:
        tb = None
      __cr__ = baml_options.get("client_registry", None)

      parsed = self.__runtime.parse_llm_response(
        "ExtractNDA",
        llm_response,
        types,
        types,
        partial_types,
        False,
        self.__ctx_manager.get(),
        tb,
        __cr__,
      )

      return cast(types.NDA, parsed)

    def GenerateBAML(
        self,
        llm_response: str,
        baml_options: BamlCallOptions = {},
    ) -> types.Schema:
      __tb__ = baml_options.get("tb", None)
      if __tb__ is not None:
        tb = __tb__._tb # type: ignore (we know how to use this private attribute)
      else:
        tb = None
      __cr__ = baml_options.get("client_registry", None)

      parsed = self.__runtime.parse_llm_response(
        "GenerateBAML",
        llm_response,
        types,
        types,
        partial_types,
        False,
        self.__ctx_manager.get(),
        tb,
        __cr__,
      )

      return cast(types.Schema, parsed)

    def TrackDeadlines(
        self,
        llm_response: str,
        baml_options: BamlCallOptions = {},
    ) -> types.DeadlineReport:
      __tb__ = baml_options.get("tb", None)
      if __tb__ is not None:
        tb = __tb__._tb # type: ignore (we know how to use this private attribute)
      else:
        tb = None
      __cr__ = baml_options.get("client_registry", None)

      parsed = self.__runtime.parse_llm_response(
        "TrackDeadlines",
        llm_response,
        types,
        types,
        partial_types,
        False,
        self.__ctx_manager.get(),
        tb,
        __cr__,
      )

      return cast(types.DeadlineReport, parsed)



class LlmStreamParser:
    __runtime: baml_py.BamlRuntime
    __ctx_manager: baml_py.BamlCtxManager

    def __init__(self, runtime: baml_py.BamlRuntime, ctx_manager: baml_py.BamlCtxManager):
      self.__runtime = runtime
      self.__ctx_manager = ctx_manager


    def AnalyzeNDARisks(
        self,
        llm_response: str,
        baml_options: BamlCallOptions = {},
    ) -> partial_types.RiskAnalysis:
      __tb__ = baml_options.get("tb", None)
      if __tb__ is not None:
        tb = __tb__._tb # type: ignore (we know how to use this private attribute)
      else:
        tb = None
      __cr__ = baml_options.get("client_registry", None)

      parsed = self.__runtime.parse_llm_response(
        "AnalyzeNDARisks",
        llm_response,
        types,
        types,
        partial_types,
        True,
        self.__ctx_manager.get(),
        tb,
        __cr__,
      )

      return cast(partial_types.RiskAnalysis, parsed)

    def ExecuteBAML(
        self,
        llm_response: str,
        baml_options: BamlCallOptions = {},
    ) -> partial_types.Response:
      __tb__ = baml_options.get("tb", None)
      if __tb__ is not None:
        tb = __tb__._tb # type: ignore (we know how to use this private attribute)
      else:
        tb = None
      __cr__ = baml_options.get("client_registry", None)

      parsed = self.__runtime.parse_llm_response(
        "ExecuteBAML",
        llm_response,
        types,
        types,
        partial_types,
        True,
        self.__ctx_manager.get(),
        tb,
        __cr__,
      )

      return cast(partial_types.Response, parsed)

    def ExtractNDA(
        self,
        llm_response: str,
        baml_options: BamlCallOptions = {},
    ) -> partial_types.NDA:
      __tb__ = baml_options.get("tb", None)
      if __tb__ is not None:
        tb = __tb__._tb # type: ignore (we know how to use this private attribute)
      else:
        tb = None
      __cr__ = baml_options.get("client_registry", None)

      parsed = self.__runtime.parse_llm_response(
        "ExtractNDA",
        llm_response,
        types,
        types,
        partial_types,
        True,
        self.__ctx_manager.get(),
        tb,
        __cr__,
      )

      return cast(partial_types.NDA, parsed)

    def GenerateBAML(
        self,
        llm_response: str,
        baml_options: BamlCallOptions = {},
    ) -> partial_types.Schema:
      __tb__ = baml_options.get("tb", None)
      if __tb__ is not None:
        tb = __tb__._tb # type: ignore (we know how to use this private attribute)
      else:
        tb = None
      __cr__ = baml_options.get("client_registry", None)

      parsed = self.__runtime.parse_llm_response(
        "GenerateBAML",
        llm_response,
        types,
        types,
        partial_types,
        True,
        self.__ctx_manager.get(),
        tb,
        __cr__,
      )

      return cast(partial_types.Schema, parsed)

    def TrackDeadlines(
        self,
        llm_response: str,
        baml_options: BamlCallOptions = {},
    ) -> partial_types.DeadlineReport:
      __tb__ = baml_options.get("tb", None)
      if __tb__ is not None:
        tb = __tb__._tb # type: ignore (we know how to use this private attribute)
      else:
        tb = None
      __cr__ = baml_options.get("client_registry", None)

      parsed = self.__runtime.parse_llm_response(
        "TrackDeadlines",
        llm_response,
        types,
        types,
        partial_types,
        True,
        self.__ctx_manager.get(),
        tb,
        __cr__,
      )

      return cast(partial_types.DeadlineReport, parsed)



__all__ = ["LlmResponseParser", "LlmStreamParser"]
