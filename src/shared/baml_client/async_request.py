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
from typing import Any, Dict, List, Literal, Optional, Type, TypedDict, Union

import baml_py
from typing_extensions import NotRequired

from . import types
from .type_builder import TypeBuilder
from .types import Check, Checked


class BamlCallOptions(TypedDict, total=False):
    tb: NotRequired[TypeBuilder]
    client_registry: NotRequired[baml_py.baml_py.ClientRegistry]


class AsyncHttpRequest:
    __runtime: baml_py.BamlRuntime
    __ctx_manager: baml_py.BamlCtxManager

    def __init__(self, runtime: baml_py.BamlRuntime, ctx_manager: baml_py.BamlCtxManager):
      self.__runtime = runtime
      self.__ctx_manager = ctx_manager


    async def AnalyzeNDARisks(
        self,
        nda: types.NDA,
        baml_options: BamlCallOptions = {},
    ) -> baml_py.HTTPRequest:
      __tb__ = baml_options.get("tb", None)
      if __tb__ is not None:
        tb = __tb__._tb # type: ignore (we know how to use this private attribute)
      else:
        tb = None
      __cr__ = baml_options.get("client_registry", None)

      return await self.__runtime.build_request(
        "AnalyzeNDARisks",
        {
          "nda": nda,
        },
        self.__ctx_manager.get(),
        tb,
        __cr__,
        False,
      )

    async def ExecuteBAML(
        self,
        content: Union[str, baml_py.Image, baml_py.Audio, List[baml_py.Image]],
        baml_options: BamlCallOptions = {},
    ) -> baml_py.HTTPRequest:
      __tb__ = baml_options.get("tb", None)
      if __tb__ is not None:
        tb = __tb__._tb # type: ignore (we know how to use this private attribute)
      else:
        tb = None
      __cr__ = baml_options.get("client_registry", None)

      return await self.__runtime.build_request(
        "ExecuteBAML",
        {
          "content": content,
        },
        self.__ctx_manager.get(),
        tb,
        __cr__,
        False,
      )

    async def ExtractNDA(
        self,
        document: Union[str, baml_py.Image, List[baml_py.Image]],
        baml_options: BamlCallOptions = {},
    ) -> baml_py.HTTPRequest:
      __tb__ = baml_options.get("tb", None)
      if __tb__ is not None:
        tb = __tb__._tb # type: ignore (we know how to use this private attribute)
      else:
        tb = None
      __cr__ = baml_options.get("client_registry", None)

      return await self.__runtime.build_request(
        "ExtractNDA",
        {
          "document": document,
        },
        self.__ctx_manager.get(),
        tb,
        __cr__,
        False,
      )

    async def GenerateBAML(
        self,
        content: Union[str, baml_py.Image, baml_py.Audio, List[baml_py.Image]],
        baml_options: BamlCallOptions = {},
    ) -> baml_py.HTTPRequest:
      __tb__ = baml_options.get("tb", None)
      if __tb__ is not None:
        tb = __tb__._tb # type: ignore (we know how to use this private attribute)
      else:
        tb = None
      __cr__ = baml_options.get("client_registry", None)

      return await self.__runtime.build_request(
        "GenerateBAML",
        {
          "content": content,
        },
        self.__ctx_manager.get(),
        tb,
        __cr__,
        False,
      )

    async def TrackDeadlines(
        self,
        nda: types.NDA,
        baml_options: BamlCallOptions = {},
    ) -> baml_py.HTTPRequest:
      __tb__ = baml_options.get("tb", None)
      if __tb__ is not None:
        tb = __tb__._tb # type: ignore (we know how to use this private attribute)
      else:
        tb = None
      __cr__ = baml_options.get("client_registry", None)

      return await self.__runtime.build_request(
        "TrackDeadlines",
        {
          "nda": nda,
        },
        self.__ctx_manager.get(),
        tb,
        __cr__,
        False,
      )



class AsyncHttpStreamRequest:
    __runtime: baml_py.BamlRuntime
    __ctx_manager: baml_py.BamlCtxManager

    def __init__(self, runtime: baml_py.BamlRuntime, ctx_manager: baml_py.BamlCtxManager):
      self.__runtime = runtime
      self.__ctx_manager = ctx_manager


    async def AnalyzeNDARisks(
        self,
        nda: types.NDA,
        baml_options: BamlCallOptions = {},
    ) -> baml_py.HTTPRequest:
      __tb__ = baml_options.get("tb", None)
      if __tb__ is not None:
        tb = __tb__._tb # type: ignore (we know how to use this private attribute)
      else:
        tb = None
      __cr__ = baml_options.get("client_registry", None)

      return await self.__runtime.build_request(
        "AnalyzeNDARisks",
        {
          "nda": nda,
        },
        self.__ctx_manager.get(),
        tb,
        __cr__,
        True,
      )

    async def ExecuteBAML(
        self,
        content: Union[str, baml_py.Image, baml_py.Audio, List[baml_py.Image]],
        baml_options: BamlCallOptions = {},
    ) -> baml_py.HTTPRequest:
      __tb__ = baml_options.get("tb", None)
      if __tb__ is not None:
        tb = __tb__._tb # type: ignore (we know how to use this private attribute)
      else:
        tb = None
      __cr__ = baml_options.get("client_registry", None)

      return await self.__runtime.build_request(
        "ExecuteBAML",
        {
          "content": content,
        },
        self.__ctx_manager.get(),
        tb,
        __cr__,
        True,
      )

    async def ExtractNDA(
        self,
        document: Union[str, baml_py.Image, List[baml_py.Image]],
        baml_options: BamlCallOptions = {},
    ) -> baml_py.HTTPRequest:
      __tb__ = baml_options.get("tb", None)
      if __tb__ is not None:
        tb = __tb__._tb # type: ignore (we know how to use this private attribute)
      else:
        tb = None
      __cr__ = baml_options.get("client_registry", None)

      return await self.__runtime.build_request(
        "ExtractNDA",
        {
          "document": document,
        },
        self.__ctx_manager.get(),
        tb,
        __cr__,
        True,
      )

    async def GenerateBAML(
        self,
        content: Union[str, baml_py.Image, baml_py.Audio, List[baml_py.Image]],
        baml_options: BamlCallOptions = {},
    ) -> baml_py.HTTPRequest:
      __tb__ = baml_options.get("tb", None)
      if __tb__ is not None:
        tb = __tb__._tb # type: ignore (we know how to use this private attribute)
      else:
        tb = None
      __cr__ = baml_options.get("client_registry", None)

      return await self.__runtime.build_request(
        "GenerateBAML",
        {
          "content": content,
        },
        self.__ctx_manager.get(),
        tb,
        __cr__,
        True,
      )

    async def TrackDeadlines(
        self,
        nda: types.NDA,
        baml_options: BamlCallOptions = {},
    ) -> baml_py.HTTPRequest:
      __tb__ = baml_options.get("tb", None)
      if __tb__ is not None:
        tb = __tb__._tb # type: ignore (we know how to use this private attribute)
      else:
        tb = None
      __cr__ = baml_options.get("client_registry", None)

      return await self.__runtime.build_request(
        "TrackDeadlines",
        {
          "nda": nda,
        },
        self.__ctx_manager.get(),
        tb,
        __cr__,
        True,
      )



__all__ = ["AsyncHttpRequest", "AsyncHttpStreamRequest"]
