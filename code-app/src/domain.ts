import type { Sams_usecases } from './generated/models/Sams_usecasesModel';
import type { Sams_usecasesystems } from './generated/models/Sams_usecasesystemsModel';

export const OptionBase = 726410000;

export const Status = {
  Draft: 726410000,
  Submitted: 726410001,
  InReview: 726410002,
  NeedsInfo: 726410003,
  Approved: 726410004,
  InBuild: 726410005,
  Live: 726410006,
  Declined: 726410007,
} as const;
export type StatusValue = (typeof Status)[keyof typeof Status];

export const AgenticTool = {
  Microsoft365Copilot: 726410000,
  CopilotCowork: 726410001,
  AgentBuilder: 726410002,
  CopilotStudioStandard: 726410003,
  CopilotStudioGitHub: 726410004,
  MicrosoftFoundry: 726410005,
  PowerAutomate: 726410006,
} as const;
export type AgenticToolValue = (typeof AgenticTool)[keyof typeof AgenticTool];

export const CreditBand = {
  Included: 726410000,
  Low: 726410001,
  Medium: 726410002,
  High: 726410003,
} as const;
export type CreditBandValue = (typeof CreditBand)[keyof typeof CreditBand];

export const Level = {
  Low: 726410000,
  Medium: 726410001,
  High: 726410002,
} as const;

export const Audience = {
  Internal: 726410000,
  External: 726410001,
  Both: 726410002,
} as const;

export const UsersBand = {
  FewerThan50: 726410000,
  From50To500: 726410001,
  From500To5000: 726410002,
  MoreThan5000: 726410003,
  NotSure: 726410004,
} as const;

export const UsageFrequency = {
  Occasionally: 726410000,
  Weekly: 726410001,
  Daily: 726410002,
  ManyTimesADay: 726410003,
  NotSure: 726410004,
} as const;

export const DataSource = {
  PublicWeb: 726410000,
  DocumentsSharePoint: 726410001,
  EmailTeamsCalendar: 726410002,
  BusinessSystems: 726410003,
  NoneOrNotSure: 726410004,
} as const;

export const Capability = {
  AnswerQuestions: 726410000,
  DraftOrSummarize: 726410001,
  TakeActions: 726410002,
  RunAutonomously: 726410003,
  MultiStepJudgment: 726410004,
} as const;

export const Predictability = {
  SameSteps: 726410000,
  MostlySame: 726410001,
  VariesALot: 726410002,
  NotSure: 726410003,
} as const;

export const UsageChannel = {
  Teams: 726410000,
  Microsoft365Copilot: 726410001,
  PublicWebsite: 726410002,
  OwnAppOrPortal: 726410003,
  NotSure: 726410004,
} as const;

export const CopilotLicence = {
  YesAll: 726410000,
  Some: 726410001,
  No: 726410002,
  NotSure: 726410003,
} as const;

export const Sensitivity = {
  None: 726410000,
  Personal: 726410001,
  Financial: 726410002,
  Regulated: 726410003,
  NotSure: 726410004,
} as const;

export const Urgency = {
  Exploring: 726410000,
  Within6Months: 726410001,
  Within3Months: 726410002,
  AsSoonAsPossible: 726410003,
} as const;

export const SystemType = {
  Microsoft365: 726410000,
  DataverseDynamics: 726410001,
  SAP: 726410002,
  ServiceNow: 726410003,
  Salesforce: 726410004,
  CustomApiDatabase: 726410005,
  WebsitePortal: 726410006,
  Other: 726410007,
} as const;

export const SystemAccess = {
  Read: 726410000,
  Write: 726410001,
  ReadWrite: 726410002,
  NotSure: 726410003,
} as const;

export const YesNoUnknown = {
  Yes: 726410000,
  No: 726410001,
  NotSure: 726410002,
} as const;

export const STATUS_LABELS: Record<number, string> = {
  [Status.Draft]: 'Draft',
  [Status.Submitted]: 'Submitted',
  [Status.InReview]: 'In review',
  [Status.NeedsInfo]: 'Needs info',
  [Status.Approved]: 'Approved',
  [Status.InBuild]: 'In build',
  [Status.Live]: 'Live',
  [Status.Declined]: 'Declined',
};

export const TOOL_LABELS: Record<number, string> = {
  [AgenticTool.Microsoft365Copilot]: 'Microsoft 365 Copilot',
  [AgenticTool.CopilotCowork]: 'Copilot Cowork',
  [AgenticTool.AgentBuilder]: 'Agent Builder (declarative agent)',
  [AgenticTool.CopilotStudioStandard]: 'Copilot Studio — Standard harness',
  [AgenticTool.CopilotStudioGitHub]: 'Copilot Studio — GitHub Copilot harness',
  [AgenticTool.MicrosoftFoundry]: 'Microsoft Foundry',
  [AgenticTool.PowerAutomate]: 'No agent needed — Power Automate / workflow',
};

export const CREDIT_LABELS: Record<number, string> = {
  [CreditBand.Included]: 'Included (about 0)',
  [CreditBand.Low]: 'Low',
  [CreditBand.Medium]: 'Medium',
  [CreditBand.High]: 'High',
};

export const LEVEL_LABELS: Record<number, string> = {
  [Level.Low]: 'Low',
  [Level.Medium]: 'Medium',
  [Level.High]: 'High',
};

export const AUDIENCE_LABELS: Record<number, string> = {
  [Audience.Internal]: 'Internal (employees)',
  [Audience.External]: 'External (customers, partners, public)',
  [Audience.Both]: 'Both',
};

export const USERS_BAND_LABELS: Record<number, string> = {
  [UsersBand.FewerThan50]: 'Fewer than 50',
  [UsersBand.From50To500]: '50 to 500',
  [UsersBand.From500To5000]: '500 to 5,000',
  [UsersBand.MoreThan5000]: 'More than 5,000',
  [UsersBand.NotSure]: 'Not sure',
};

export const FREQUENCY_LABELS: Record<number, string> = {
  [UsageFrequency.Occasionally]: 'Occasionally',
  [UsageFrequency.Weekly]: 'Weekly',
  [UsageFrequency.Daily]: 'Daily',
  [UsageFrequency.ManyTimesADay]: 'Many times a day',
  [UsageFrequency.NotSure]: 'Not sure',
};

export const DATA_SOURCE_LABELS: Record<number, string> = {
  [DataSource.PublicWeb]: 'Public web',
  [DataSource.DocumentsSharePoint]: 'Documents and SharePoint',
  [DataSource.EmailTeamsCalendar]: 'Email, Teams and calendar',
  [DataSource.BusinessSystems]: 'Business systems',
  [DataSource.NoneOrNotSure]: 'None or not sure',
};

export const CAPABILITY_LABELS: Record<number, string> = {
  [Capability.AnswerQuestions]: 'Answer questions',
  [Capability.DraftOrSummarize]: 'Draft or summarize content',
  [Capability.TakeActions]: 'Take actions in systems',
  [Capability.RunAutonomously]: 'Run on its own when something happens',
  [Capability.MultiStepJudgment]: 'Multi-step tasks with judgment',
};

export const PREDICTABILITY_LABELS: Record<number, string> = {
  [Predictability.SameSteps]: 'Same steps every time',
  [Predictability.MostlySame]: 'Mostly the same, some exceptions',
  [Predictability.VariesALot]: 'Varies a lot case by case',
  [Predictability.NotSure]: 'Not sure',
};

export const CHANNEL_LABELS: Record<number, string> = {
  [UsageChannel.Teams]: 'Microsoft Teams',
  [UsageChannel.Microsoft365Copilot]: 'Microsoft 365 Copilot',
  [UsageChannel.PublicWebsite]: 'Public website',
  [UsageChannel.OwnAppOrPortal]: 'Our own app or portal',
  [UsageChannel.NotSure]: 'Not sure',
};

export const LICENCE_LABELS: Record<number, string> = {
  [CopilotLicence.YesAll]: 'Yes, all users',
  [CopilotLicence.Some]: 'Some users',
  [CopilotLicence.No]: 'No',
  [CopilotLicence.NotSure]: 'Not sure',
};

export const SENSITIVITY_LABELS: Record<number, string> = {
  [Sensitivity.None]: 'No sensitive data',
  [Sensitivity.Personal]: 'Personal information',
  [Sensitivity.Financial]: 'Financial information',
  [Sensitivity.Regulated]: 'Regulated or confidential',
  [Sensitivity.NotSure]: 'Not sure',
};

export const URGENCY_LABELS: Record<number, string> = {
  [Urgency.Exploring]: 'Exploring the idea',
  [Urgency.Within6Months]: 'Within 6 months',
  [Urgency.Within3Months]: 'Within 3 months',
  [Urgency.AsSoonAsPossible]: 'As soon as possible',
};

export const SYSTEM_TYPE_LABELS: Record<number, string> = {
  [SystemType.Microsoft365]: 'Microsoft 365 app',
  [SystemType.DataverseDynamics]: 'Dataverse or Dynamics 365',
  [SystemType.SAP]: 'SAP',
  [SystemType.ServiceNow]: 'ServiceNow',
  [SystemType.Salesforce]: 'Salesforce',
  [SystemType.CustomApiDatabase]: 'Custom API or database',
  [SystemType.WebsitePortal]: 'Website or portal',
  [SystemType.Other]: 'Other',
};

export const SYSTEM_ACCESS_LABELS: Record<number, string> = {
  [SystemAccess.Read]: 'Read',
  [SystemAccess.Write]: 'Write',
  [SystemAccess.ReadWrite]: 'Read and write',
  [SystemAccess.NotSure]: 'Not sure',
};

export const YES_NO_UNKNOWN_LABELS: Record<number, string> = {
  [YesNoUnknown.Yes]: 'Yes',
  [YesNoUnknown.No]: 'No',
  [YesNoUnknown.NotSure]: 'Not sure',
};

export const STATUS_ORDER: StatusValue[] = [
  Status.Submitted,
  Status.InReview,
  Status.NeedsInfo,
  Status.Approved,
  Status.InBuild,
  Status.Live,
  Status.Declined,
  Status.Draft,
];

export const TOOL_OPTIONS = Object.values(AgenticTool);
export const STATUS_OPTIONS = STATUS_ORDER;
export const CREDIT_OPTIONS = Object.values(CreditBand);
export const AUDIENCE_OPTIONS = Object.values(Audience);

export const MS_COLORS = {
  red: '#F25022',
  green: '#7FBA00',
  blue: '#00A4EF',
  yellow: '#FFB900',
  grey: '#737373',
} as const;

export const STATUS_COLORS: Record<number, string> = {
  [Status.Draft]: MS_COLORS.grey,
  [Status.Submitted]: MS_COLORS.blue,
  [Status.InReview]: MS_COLORS.red,
  [Status.NeedsInfo]: MS_COLORS.yellow,
  [Status.Approved]: MS_COLORS.green,
  [Status.InBuild]: MS_COLORS.blue,
  [Status.Live]: MS_COLORS.green,
  [Status.Declined]: MS_COLORS.red,
};

export const CREDIT_COLORS: Record<number, string> = {
  [CreditBand.Included]: MS_COLORS.grey,
  [CreditBand.Low]: MS_COLORS.green,
  [CreditBand.Medium]: MS_COLORS.yellow,
  [CreditBand.High]: MS_COLORS.red,
};

export const TOOL_COLORS: Record<number, string> = {
  [AgenticTool.Microsoft365Copilot]: MS_COLORS.blue,
  [AgenticTool.CopilotCowork]: MS_COLORS.green,
  [AgenticTool.AgentBuilder]: MS_COLORS.yellow,
  [AgenticTool.CopilotStudioStandard]: MS_COLORS.red,
  [AgenticTool.CopilotStudioGitHub]: MS_COLORS.blue,
  [AgenticTool.MicrosoftFoundry]: MS_COLORS.green,
  [AgenticTool.PowerAutomate]: MS_COLORS.grey,
};

export const DEFAULT_TOOL_GUIDE_URL =
  'https://blue-hill-0cabcc90f.5.azurestaticapps.net/which-agentic-tool.html';
export const DEFAULT_CREDITS_GUIDE_URL =
  'https://blue-hill-0cabcc90f.5.azurestaticapps.net/copilot-studio-credits-explainer-extended.html';

export interface TargetSystem {
  id: string;
  useCaseId: string | null;
  name: string;
  type: number | null;
  access: number | null;
  connectorAvailable: number | null;
}

export interface UseCaseRecord {
  raw: Sams_usecases;
  id: string;
  number: string | null;
  title: string;
  submitterEmail: string;
  createdById: string | null;
  problemStatement: string | null;
  desiredOutcome: string | null;
  currentProcess: string | null;
  exampleRequest: string | null;
  hoursSavedPerMonth: number | null;
  audience: number | null;
  usersBand: number | null;
  usageFrequency: number | null;
  dataSources: number[];
  capabilities: number[];
  predictability: number | null;
  documentHeavy: boolean | null;
  usageChannel: number | null;
  copilotLicence: number | null;
  sensitivity: number | null;
  urgency: number | null;
  recommendedTool: number | null;
  alternativeTool: number | null;
  rationale: string | null;
  creditBand: number | null;
  estimatedMonthlyCredits: number | null;
  creditDrivers: string | null;
  complexity: number | null;
  confidence: number | null;
  assumptions: string | null;
  valueScore: number | null;
  feasibilityScore: number | null;
  priorityScore: number | null;
  rubricVersion: string | null;
  status: number | null;
  reviewedBy: string | null;
  finalTool: number | null;
  reviewerNotes: string | null;
  infoNeeded: string | null;
  decisionDate: string | null;
  conversationSummary: string | null;
  conversationId: string | null;
  createdOn: string | null;
  systems: TargetSystem[];
}

export interface AppConfig {
  intakeAgentUrl: string;
  toolGuideUrl: string;
  creditsGuideUrl: string;
}

function text(value: string | undefined): string | null {
  return value && value.trim().length > 0 ? value : null;
}

function numeric(value: unknown): number | null {
  return typeof value === 'number' ? value : null;
}

export function parseMultiChoice(value: string | undefined): number[] {
  if (!value) return [];
  return value
    .split(',')
    .map((part) => Number(part.trim()))
    .filter((part) => Number.isFinite(part));
}

export function labelFor(
  labels: Record<number, string>,
  value: number | null | undefined,
  fallback = 'Not set',
): string {
  return typeof value === 'number' ? (labels[value] ?? fallback) : fallback;
}

export function labelsFor(labels: Record<number, string>, values: number[]): string[] {
  return values.map((value) => labels[value] ?? String(value));
}

export function toTargetSystem(row: Sams_usecasesystems): TargetSystem {
  return {
    id: row.sams_usecasesystemid,
    useCaseId: row._sams_usecaseid_value ?? null,
    name: text(row.sams_name) ?? 'Unnamed system',
    type: numeric(row.sams_systemtype),
    access: numeric(row.sams_access),
    connectorAvailable: numeric(row.sams_connectoravailable),
  };
}

export function toUseCase(row: Sams_usecases, systems: TargetSystem[]): UseCaseRecord {
  return {
    raw: row,
    id: row.sams_usecaseid,
    number: text(row.sams_usecasenumber),
    title: text(row.sams_name) ?? 'Untitled idea',
    submitterEmail: text(row.sams_submitteremail) ?? '',
    createdById: text(row._createdby_value),
    problemStatement: text(row.sams_problemstatement),
    desiredOutcome: text(row.sams_desiredoutcome),
    currentProcess: text(row.sams_currentprocess),
    exampleRequest: text(row.sams_examplerequest),
    hoursSavedPerMonth: numeric(row.sams_hourssavedpermonth),
    audience: numeric(row.sams_audience),
    usersBand: numeric(row.sams_usersband),
    usageFrequency: numeric(row.sams_usagefrequency),
    dataSources: parseMultiChoice(row.sams_datasources),
    capabilities: parseMultiChoice(row.sams_capabilities),
    predictability: numeric(row.sams_predictability),
    documentHeavy: typeof row.sams_documentheavy === 'boolean' ? row.sams_documentheavy : null,
    usageChannel: numeric(row.sams_usagechannel),
    copilotLicence: numeric(row.sams_copilotlicence),
    sensitivity: numeric(row.sams_sensitivity),
    urgency: numeric(row.sams_urgency),
    recommendedTool: numeric(row.sams_recommendedtool),
    alternativeTool: numeric(row.sams_alternativetool),
    rationale: text(row.sams_rationale),
    creditBand: numeric(row.sams_creditband),
    estimatedMonthlyCredits: numeric(row.sams_estimatedmonthlycredits),
    creditDrivers: text(row.sams_creditdrivers),
    complexity: numeric(row.sams_complexity),
    confidence: numeric(row.sams_confidence),
    assumptions: text(row.sams_assumptions),
    valueScore: numeric(row.sams_valuescore),
    feasibilityScore: numeric(row.sams_feasibilityscore),
    priorityScore: numeric(row.sams_priorityscore),
    rubricVersion: text(row.sams_rubricversion),
    status: numeric(row.sams_status),
    reviewedBy: text(row.sams_reviewedby),
    finalTool: numeric(row.sams_finaltool),
    reviewerNotes: text(row.sams_reviewernotes),
    infoNeeded: text(row.sams_infoneeded),
    decisionDate: text(row.sams_decisiondate),
    conversationSummary: text(row.sams_conversationsummary),
    conversationId: text(row.sams_conversationid),
    createdOn: text(row.createdon),
    systems: systems.filter((system) => system.useCaseId === row.sams_usecaseid),
  };
}
