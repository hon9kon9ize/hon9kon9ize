export const mockChrome = {
  action: {
    onClicked: {
      addListener: _callback => {},
    },
  },
  runtime: {
    onMessage: {
      addListener: _callback => {},
      removeListener: _callback => {},
    },
  },
  tabs: {
    sendMessage: (_tabId: number, _message: any) => {
      return Promise.resolve();
    },
  },
} as typeof chrome;
