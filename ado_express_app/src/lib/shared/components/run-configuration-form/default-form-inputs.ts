import type { IInputSettings } from '../../../models/interfaces/input-settings.interface';

export const defaultFormInputs = {
  dd: {
    bindValue: null,
    required: true,
    show: true,
  } as IInputSettings,
  org_url: {
    bindValue: '',
    required: true,
    show: true,
  } as IInputSettings,
  pat: {
    bindValue: '',
    required: true,
    show: true,
  } as IInputSettings,
  queries: {
    bindValue: '',
    required: true,
    show: true,
  } as IInputSettings,
  rnf: {
    bindValue: 'Release-$(rev:r)',
    required: true,
    show: true,
  } as IInputSettings,
  rte: {
    bindValue: '',
    required: true,
    show: true,
  } as IInputSettings,
  rse: {
    bindValue: '',
    required: true,
    show: true,
  } as IInputSettings
};
