from __future__ import annotations

import logging

from datatalk.agents import (
    QuestionUnderstandingAgent,
    SchemaExplorerAgent,
    SQLWriterAgent,
    SQLRetryAgent,
    ExplanationAgent,
)
from datatalk.database.connection import db_manager
from datatalk.guardrails import SQLSafety
from datatalk.llm import BaseLLMProvider, get_llm
from datatalk.memory import SQLMemoryService
from datatalk.services import (
    RelationshipGraph,
    SQLExecutor,
    SchemaService,
    schema_service,
)
from datatalk.graph.workflow import DataTalkGraph
from datatalk.graph.nodes import GraphNodes, set_container


logger = logging.getLogger(__name__)


class Container:
    def __init__(self):
        self._initialized = False
        self._llm: BaseLLMProvider | None = None
        self._schema_service: SchemaService = schema_service
        self._relationship_graph: RelationshipGraph | None = None
        self._sql_safety: SQLSafety | None = None
        self._sql_executor: SQLExecutor | None = None
        self._sql_memory: SQLMemoryService | None = None
        self._question_agent = None
        self._schema_explorer = None
        self._sql_writer = None
        self._sql_retry = None
        self._explanation_agent = None
        self._graph: DataTalkGraph | None = None

    def initialize(self, llm_provider: BaseLLMProvider | None = None, force: bool = False):
        if self._initialized and not force:
            return

        if force:
            self._reset()

        logger.info("Initializing DataTalk...")

        self._create_llm(llm_provider)
        self._create_services()
        self._create_agents()
        self._create_graph()

        self._initialized = True

        logger.info("DataTalk initialized.")

    def _reset(self) -> None:
        self._initialized = False
        self._llm = None
        self._relationship_graph = None
        self._sql_safety = None
        self._sql_executor = None
        self._sql_memory = None
        self._question_agent = None
        self._schema_explorer = None
        self._sql_writer = None
        self._sql_retry = None
        self._explanation_agent = None
        self._graph = None

    def _create_llm(self, llm_provider: BaseLLMProvider | None = None):
        self._llm = llm_provider or get_llm()

    def _create_services(self):
        self._relationship_graph = RelationshipGraph(self._schema_service)
        self._sql_safety = SQLSafety()
        self._sql_executor = SQLExecutor(db=db_manager, safety=self._sql_safety)
        self._sql_memory = SQLMemoryService()

    def _create_agents(self):
        assert self._llm is not None
        assert self._relationship_graph is not None

        self._question_agent = QuestionUnderstandingAgent(llm=self._llm)
        self._schema_explorer = SchemaExplorerAgent(
            llm=self._llm,
            schema_service=self._schema_service,
            relationship_graph=self._relationship_graph,
        )
        self._sql_writer = SQLWriterAgent(
            llm=self._llm,
            schema_service=self._schema_service,
        )
        self._sql_retry = SQLRetryAgent(llm=self._llm)
        self._explanation_agent = ExplanationAgent(llm=self._llm)

    def _create_graph(self):
        set_container(self)

        nodes = GraphNodes(
            question_agent=self._question_agent,
            schema_explorer=self._schema_explorer,
            sql_writer=self._sql_writer,
            sql_executor=self._sql_executor,
            sql_retry=self._sql_retry,
            explanation_agent=self._explanation_agent,
            memory_service=self._sql_memory,
        )

        self._graph = DataTalkGraph(nodes)

    @property
    def graph(self):
        assert self._graph is not None
        return self._graph

    @property
    def question_agent(self):
        assert self._question_agent is not None
        return self._question_agent

    @property
    def schema_explorer(self):
        assert self._schema_explorer is not None
        return self._schema_explorer

    @property
    def sql_writer(self):
        assert self._sql_writer is not None
        return self._sql_writer

    @property
    def sql_retry(self):
        assert self._sql_retry is not None
        return self._sql_retry

    @property
    def explanation_agent(self):
        assert self._explanation_agent is not None
        return self._explanation_agent

    @property
    def sql_executor(self):
        assert self._sql_executor is not None
        return self._sql_executor

    @property
    def schema_service(self):
        return self._schema_service

    @property
    def sql_memory(self):
        assert self._sql_memory is not None
        return self._sql_memory


container = Container()
