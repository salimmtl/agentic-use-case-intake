import { getContext } from '@microsoft/power-apps/app';
import { APP_CONFIG } from './config.generated';
import { Sams_usecasesService } from './generated/services/Sams_usecasesService';
import { Sams_usecasesystemsService } from './generated/services/Sams_usecasesystemsService';
import type { Sams_usecases } from './generated/models/Sams_usecasesModel';
import type { Sams_usecasesystems } from './generated/models/Sams_usecasesystemsModel';
import { Status, type AppConfig, type UseCaseRecord, toTargetSystem, toUseCase } from './domain';

const USECASE_SELECT = [
  'sams_usecaseid',
  'sams_name',
  'sams_usecasenumber',
  'sams_submitteremail',
  '_createdby_value',
  'sams_problemstatement',
  'sams_desiredoutcome',
  'sams_currentprocess',
  'sams_examplerequest',
  'sams_hourssavedpermonth',
  'sams_audience',
  'sams_usersband',
  'sams_usagefrequency',
  'sams_datasources',
  'sams_capabilities',
  'sams_predictability',
  'sams_documentheavy',
  'sams_usagechannel',
  'sams_copilotlicence',
  'sams_sensitivity',
  'sams_urgency',
  'sams_recommendedtool',
  'sams_alternativetool',
  'sams_rationale',
  'sams_creditband',
  'sams_estimatedmonthlycredits',
  'sams_creditdrivers',
  'sams_complexity',
  'sams_confidence',
  'sams_assumptions',
  'sams_valuescore',
  'sams_feasibilityscore',
  'sams_priorityscore',
  'sams_rubricversion',
  'sams_status',
  'sams_reviewedby',
  'sams_finaltool',
  'sams_reviewernotes',
  'sams_infoneeded',
  'sams_decisiondate',
  'sams_conversationsummary',
  'sams_conversationid',
  'createdon',
];

const SYSTEM_SELECT = [
  'sams_usecasesystemid',
  'sams_name',
  'sams_systemtype',
  'sams_access',
  'sams_connectoravailable',
  '_sams_usecaseid_value',
];

export async function loadWorkspace(): Promise<UseCaseRecord[]> {
  const [useCasesResult, systemsResult] = await Promise.all([
    Sams_usecasesService.getAll({ select: USECASE_SELECT, orderBy: ['createdon desc'], top: 500 }),
    Sams_usecasesystemsService.getAll({ select: SYSTEM_SELECT, orderBy: ['sams_name asc'], top: 1000 }),
  ]);

  if (!useCasesResult.success) {
    throw new Error(useCasesResult.error?.message ?? 'Could not load use cases from Dataverse.');
  }
  if (!systemsResult.success) {
    throw new Error(systemsResult.error?.message ?? 'Could not load target systems from Dataverse.');
  }

  const systems = (systemsResult.data ?? []).map((row: Sams_usecasesystems) => toTargetSystem(row));
  return (useCasesResult.data ?? []).map((row: Sams_usecases) => toUseCase(row, systems));
}

export interface ReviewUpdate {
  status: number;
  finalTool?: number;
  reviewerNotes?: string;
  infoNeeded?: string;
  reviewerEmail: string;
}

function localDateOnly(date = new Date()): string {
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, '0');
  const day = String(date.getDate()).padStart(2, '0');
  return `${year}-${month}-${day}`;
}

export async function saveReview(useCase: UseCaseRecord, update: ReviewUpdate): Promise<void> {
  const decisionStatuses = [Status.Approved, Status.Declined];
  const fields: Record<string, unknown> = {
    sams_status: update.status,
    sams_reviewedby: update.reviewerEmail,
    sams_finaltool: update.finalTool,
    sams_reviewernotes: update.reviewerNotes ?? '',
    sams_infoneeded: update.infoNeeded ?? '',
  };

  if (update.status !== useCase.status && decisionStatuses.includes(update.status as never)) {
    fields.sams_decisiondate = localDateOnly();
  }

  const result = await Sams_usecasesService.update(useCase.id, fields as never);
  if (!result.success) {
    throw new Error(result.error?.message ?? 'Dataverse rejected the review update.');
  }
}

export async function getSignedInEmail(): Promise<string> {
  try {
    const context = await getContext();
    return context.user.userPrincipalName ?? '';
  } catch {
    return '';
  }
}

export async function loadAppConfig(): Promise<AppConfig> {
  return APP_CONFIG;
}
