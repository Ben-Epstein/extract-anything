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
import pprint
from typing import Any, Dict, List, Literal, Optional, Type, TypedDict, TypeVar, Union, cast

import baml_py
from pydantic import BaseModel, ValidationError, create_model
from typing_extensions import NotRequired

from . import partial_types, types
from .globals import (
    DO_NOT_USE_DIRECTLY_UNLESS_YOU_KNOW_WHAT_YOURE_DOING_CTX,
    DO_NOT_USE_DIRECTLY_UNLESS_YOU_KNOW_WHAT_YOURE_DOING_RUNTIME,
)
from .parser import LlmResponseParser, LlmStreamParser
from .sync_request import HttpRequest, HttpStreamRequest
from .type_builder import TypeBuilder
from .types import Check, Checked

OutputType = TypeVar('OutputType')


# Define the TypedDict with optional parameters having default values
class BamlCallOptions(TypedDict, total=False):
    tb: NotRequired[TypeBuilder]
    client_registry: NotRequired[baml_py.baml_py.ClientRegistry]
    collector: NotRequired[Union[baml_py.baml_py.Collector, List[baml_py.baml_py.Collector]]]


class BamlSyncClient:
    __runtime: baml_py.BamlRuntime
    __ctx_manager: baml_py.BamlCtxManager
    __stream_client: "BamlStreamClient"
    __http_request: "HttpRequest"
    __http_stream_request: "HttpStreamRequest"
    __llm_response_parser: LlmResponseParser
    __baml_options: BamlCallOptions

    def __init__(self, runtime: baml_py.BamlRuntime, ctx_manager: baml_py.BamlCtxManager, baml_options: Optional[BamlCallOptions] = None):
      self.__runtime = runtime
      self.__ctx_manager = ctx_manager
      self.__stream_client = BamlStreamClient(self.__runtime, self.__ctx_manager, baml_options)
      self.__http_request = HttpRequest(self.__runtime, self.__ctx_manager)
      self.__http_stream_request = HttpStreamRequest(self.__runtime, self.__ctx_manager)
      self.__llm_response_parser = LlmResponseParser(self.__runtime, self.__ctx_manager)
      self.__llm_stream_parser = LlmStreamParser(self.__runtime, self.__ctx_manager)
      self.__baml_options = baml_options or {}

    @property
    def stream(self):
      return self.__stream_client

    @property
    def request(self):
      return self.__http_request

    @property
    def stream_request(self):
      return self.__http_stream_request

    @property
    def parse(self):
      return self.__llm_response_parser

    @property
    def parse_stream(self):
      return self.__llm_stream_parser

    def with_options(
      self,
      tb: Optional[TypeBuilder] = None,
      client_registry: Optional[baml_py.baml_py.ClientRegistry] = None,
      collector: Optional[Union[baml_py.baml_py.Collector, List[baml_py.baml_py.Collector]]] = None,
    ) -> "BamlSyncClient":
      """Returns a new instance of BamlSyncClient with explicitly typed baml options
      for Python 3.8 compatibility.
      """
      new_options: BamlCallOptions = self.__baml_options.copy()

      # Override if any keyword arguments were provided.
      if tb is not None:
          new_options["tb"] = tb
      if client_registry is not None:
          new_options["client_registry"] = client_registry
      if collector is not None:
          new_options["collector"] = collector
      return BamlSyncClient(self.__runtime, self.__ctx_manager, new_options)


    def AnalyzeNDARisks(
        self,
        nda: types.NDA,
        baml_options: BamlCallOptions = {},
    ) -> types.RiskAnalysis:
      options: BamlCallOptions = {**self.__baml_options, **(baml_options or {})}
      __tb__ = options.get("tb", None)
      if __tb__ is not None:
        tb = __tb__._tb # type: ignore (we know how to use this private attribute)
      else:
        tb = None
      __cr__ = options.get("client_registry", None)
      collector = options.get("collector", None)
      collectors = collector if isinstance(collector, list) else [collector] if collector is not None else []

      raw = self.__runtime.call_function_sync(
        "AnalyzeNDARisks",
        {
          "nda": nda,
        },
        self.__ctx_manager.get(),
        tb,
        __cr__,
        collectors,
      )
      return cast(types.RiskAnalysis, raw.cast_to(types, types, partial_types, False))

    def ExecuteBAML(
        self,
        content: Union[str, baml_py.Image, baml_py.Audio, List[baml_py.Image]],
        baml_options: BamlCallOptions = {},
    ) -> types.Response:
      options: BamlCallOptions = {**self.__baml_options, **(baml_options or {})}
      __tb__ = options.get("tb", None)
      if __tb__ is not None:
        tb = __tb__._tb # type: ignore (we know how to use this private attribute)
      else:
        tb = None
      __cr__ = options.get("client_registry", None)
      collector = options.get("collector", None)
      collectors = collector if isinstance(collector, list) else [collector] if collector is not None else []

      raw = self.__runtime.call_function_sync(
        "ExecuteBAML",
        {
          "content": content,
        },
        self.__ctx_manager.get(),
        tb,
        __cr__,
        collectors,
      )
      return cast(types.Response, raw.cast_to(types, types, partial_types, False))

    def ExtractNDA(
        self,
        document: Union[str, baml_py.Image, List[baml_py.Image]],
        baml_options: BamlCallOptions = {},
    ) -> types.NDA:
      options: BamlCallOptions = {**self.__baml_options, **(baml_options or {})}
      __tb__ = options.get("tb", None)
      if __tb__ is not None:
        tb = __tb__._tb # type: ignore (we know how to use this private attribute)
      else:
        tb = None
      __cr__ = options.get("client_registry", None)
      collector = options.get("collector", None)
      collectors = collector if isinstance(collector, list) else [collector] if collector is not None else []

      raw = self.__runtime.call_function_sync(
        "ExtractNDA",
        {
          "document": document,
        },
        self.__ctx_manager.get(),
        tb,
        __cr__,
        collectors,
      )
      return cast(types.NDA, raw.cast_to(types, types, partial_types, False))

    def GenerateBAML(
        self,
        content: Union[str, baml_py.Image, baml_py.Audio, List[baml_py.Image]],
        baml_options: BamlCallOptions = {},
    ) -> types.Schema:
      options: BamlCallOptions = {**self.__baml_options, **(baml_options or {})}
      __tb__ = options.get("tb", None)
      if __tb__ is not None:
        tb = __tb__._tb # type: ignore (we know how to use this private attribute)
      else:
        tb = None
      __cr__ = options.get("client_registry", None)
      collector = options.get("collector", None)
      collectors = collector if isinstance(collector, list) else [collector] if collector is not None else []

      raw = self.__runtime.call_function_sync(
        "GenerateBAML",
        {
          "content": content,
        },
        self.__ctx_manager.get(),
        tb,
        __cr__,
        collectors,
      )
      return cast(types.Schema, raw.cast_to(types, types, partial_types, False))

    def TrackDeadlines(
        self,
        nda: types.NDA,
        baml_options: BamlCallOptions = {},
    ) -> types.DeadlineReport:
      options: BamlCallOptions = {**self.__baml_options, **(baml_options or {})}
      __tb__ = options.get("tb", None)
      if __tb__ is not None:
        tb = __tb__._tb # type: ignore (we know how to use this private attribute)
      else:
        tb = None
      __cr__ = options.get("client_registry", None)
      collector = options.get("collector", None)
      collectors = collector if isinstance(collector, list) else [collector] if collector is not None else []

      raw = self.__runtime.call_function_sync(
        "TrackDeadlines",
        {
          "nda": nda,
        },
        self.__ctx_manager.get(),
        tb,
        __cr__,
        collectors,
      )
      return cast(types.DeadlineReport, raw.cast_to(types, types, partial_types, False))




class BamlStreamClient:
    __runtime: baml_py.BamlRuntime
    __ctx_manager: baml_py.BamlCtxManager
    __baml_options: BamlCallOptions
    def __init__(self, runtime: baml_py.BamlRuntime, ctx_manager: baml_py.BamlCtxManager, baml_options: Optional[BamlCallOptions] = None):
      self.__runtime = runtime
      self.__ctx_manager = ctx_manager
      self.__baml_options = baml_options or {}


    def AnalyzeNDARisks(
        self,
        nda: types.NDA,
        baml_options: BamlCallOptions = {},
    ) -> baml_py.BamlSyncStream[partial_types.RiskAnalysis, types.RiskAnalysis]:
      options: BamlCallOptions = {**self.__baml_options, **(baml_options or {})}
      __tb__ = options.get("tb", None)
      if __tb__ is not None:
        tb = __tb__._tb # type: ignore (we know how to use this private attribute)
      else:
        tb = None
      __cr__ = options.get("client_registry", None)
      collector = options.get("collector", None)
      collectors = collector if isinstance(collector, list) else [collector] if collector is not None else []

      raw = self.__runtime.stream_function_sync(
        "AnalyzeNDARisks",
        {
          "nda": nda,
        },
        None,
        self.__ctx_manager.get(),
        tb,
        __cr__,
        collectors,
      )

      return baml_py.BamlSyncStream[partial_types.RiskAnalysis, types.RiskAnalysis](
        raw,
        lambda x: cast(partial_types.RiskAnalysis, x.cast_to(types, types, partial_types, True)),
        lambda x: cast(types.RiskAnalysis, x.cast_to(types, types, partial_types, False)),
        self.__ctx_manager.get(),
      )

    def ExecuteBAML(
        self,
        content: Union[str, baml_py.Image, baml_py.Audio, List[baml_py.Image]],
        baml_options: BamlCallOptions = {},
    ) -> baml_py.BamlSyncStream[partial_types.Response, types.Response]:
      options: BamlCallOptions = {**self.__baml_options, **(baml_options or {})}
      __tb__ = options.get("tb", None)
      if __tb__ is not None:
        tb = __tb__._tb # type: ignore (we know how to use this private attribute)
      else:
        tb = None
      __cr__ = options.get("client_registry", None)
      collector = options.get("collector", None)
      collectors = collector if isinstance(collector, list) else [collector] if collector is not None else []

      raw = self.__runtime.stream_function_sync(
        "ExecuteBAML",
        {
          "content": content,
        },
        None,
        self.__ctx_manager.get(),
        tb,
        __cr__,
        collectors,
      )

      return baml_py.BamlSyncStream[partial_types.Response, types.Response](
        raw,
        lambda x: cast(partial_types.Response, x.cast_to(types, types, partial_types, True)),
        lambda x: cast(types.Response, x.cast_to(types, types, partial_types, False)),
        self.__ctx_manager.get(),
      )

    def ExtractNDA(
        self,
        document: Union[str, baml_py.Image, List[baml_py.Image]],
        baml_options: BamlCallOptions = {},
    ) -> baml_py.BamlSyncStream[partial_types.NDA, types.NDA]:
      options: BamlCallOptions = {**self.__baml_options, **(baml_options or {})}
      __tb__ = options.get("tb", None)
      if __tb__ is not None:
        tb = __tb__._tb # type: ignore (we know how to use this private attribute)
      else:
        tb = None
      __cr__ = options.get("client_registry", None)
      collector = options.get("collector", None)
      collectors = collector if isinstance(collector, list) else [collector] if collector is not None else []

      raw = self.__runtime.stream_function_sync(
        "ExtractNDA",
        {
          "document": document,
        },
        None,
        self.__ctx_manager.get(),
        tb,
        __cr__,
        collectors,
      )

      return baml_py.BamlSyncStream[partial_types.NDA, types.NDA](
        raw,
        lambda x: cast(partial_types.NDA, x.cast_to(types, types, partial_types, True)),
        lambda x: cast(types.NDA, x.cast_to(types, types, partial_types, False)),
        self.__ctx_manager.get(),
      )

    def GenerateBAML(
        self,
        content: Union[str, baml_py.Image, baml_py.Audio, List[baml_py.Image]],
        baml_options: BamlCallOptions = {},
    ) -> baml_py.BamlSyncStream[partial_types.Schema, types.Schema]:
      options: BamlCallOptions = {**self.__baml_options, **(baml_options or {})}
      __tb__ = options.get("tb", None)
      if __tb__ is not None:
        tb = __tb__._tb # type: ignore (we know how to use this private attribute)
      else:
        tb = None
      __cr__ = options.get("client_registry", None)
      collector = options.get("collector", None)
      collectors = collector if isinstance(collector, list) else [collector] if collector is not None else []

      raw = self.__runtime.stream_function_sync(
        "GenerateBAML",
        {
          "content": content,
        },
        None,
        self.__ctx_manager.get(),
        tb,
        __cr__,
        collectors,
      )

      return baml_py.BamlSyncStream[partial_types.Schema, types.Schema](
        raw,
        lambda x: cast(partial_types.Schema, x.cast_to(types, types, partial_types, True)),
        lambda x: cast(types.Schema, x.cast_to(types, types, partial_types, False)),
        self.__ctx_manager.get(),
      )

    def TrackDeadlines(
        self,
        nda: types.NDA,
        baml_options: BamlCallOptions = {},
    ) -> baml_py.BamlSyncStream[partial_types.DeadlineReport, types.DeadlineReport]:
      options: BamlCallOptions = {**self.__baml_options, **(baml_options or {})}
      __tb__ = options.get("tb", None)
      if __tb__ is not None:
        tb = __tb__._tb # type: ignore (we know how to use this private attribute)
      else:
        tb = None
      __cr__ = options.get("client_registry", None)
      collector = options.get("collector", None)
      collectors = collector if isinstance(collector, list) else [collector] if collector is not None else []

      raw = self.__runtime.stream_function_sync(
        "TrackDeadlines",
        {
          "nda": nda,
        },
        None,
        self.__ctx_manager.get(),
        tb,
        __cr__,
        collectors,
      )

      return baml_py.BamlSyncStream[partial_types.DeadlineReport, types.DeadlineReport](
        raw,
        lambda x: cast(partial_types.DeadlineReport, x.cast_to(types, types, partial_types, True)),
        lambda x: cast(types.DeadlineReport, x.cast_to(types, types, partial_types, False)),
        self.__ctx_manager.get(),
      )



b = BamlSyncClient(DO_NOT_USE_DIRECTLY_UNLESS_YOU_KNOW_WHAT_YOURE_DOING_RUNTIME, DO_NOT_USE_DIRECTLY_UNLESS_YOU_KNOW_WHAT_YOURE_DOING_CTX)

__all__ = ["b"]
