export default {
    createView: {
      title: 'Share your honest view',
      description: 'Helps me reflect on what I think of myself',
      inputPlaceholder: 'Enter your question here',
      ratingButton: 'Rating',
      yesNoButton: 'Yes/No',
      addButton: 'Add',
      suggestButton: 'Suggest',
      publishButton: 'Publish',
      alertMessage: 'Complete self review before publishing',
      publishedMessage: 'The review is published and live!',
      reviewCodeLabel: 'Review code',
      reviewLinkLabel: 'Review Link',
      copyUrlButton: 'Copy URL',
      toastSuccess: 'Survey created successfully!',
      toastError: 'Failed to create survey. Please try again.',
      copySuccess: 'Copied to clipboard!',
      copyError: 'Failed to copy to clipboard',
      errorCheckingCode:'Cannot validate the id',
      errorFetchingCodes: 'Error fetching suggestions. Please try again.',
      codeNotAvailable:'The id is already used or invalid (contains space, special characters)'
    },
    homeView: {
      title: 'Calibrate your self awareness',
      subtitle: 'Compare what you think about yourself, what others really look at you as',
      createButton: 'Create a review',
      participateTitle: 'Came here for a friend?',
      participateSubtitle: 'Share some valuable feedback to the creator and see what others are saying',
      participatePlaceholder: 'Enter review code',
      participateButton: 'Participate',
      errorMessage: 'Invalid survey code or survey not found. Please try again.',
    },
    takeSurvey: {
      previousButton: 'Previous',
      nextButton: 'Next',
      finishButton: 'Finish',
      loadingMessage: 'Loading survey...',
      submittingButton: 'Publishing...',
      errorSubmitting: 'Error submitting survey. Please try again.',
      errorFetchingCodes: 'Error fetching suggestions. Please try again.',
      missingSurveyId: 'Survey ID is missing. Please check the URL and try again.',
      surveyNotFound: 'Survey not found. Please check the survey ID and try again.',
      errorLoading: 'An error occurred while loading the survey. Please try again later.',
      unexpectedError: 'An unexpected error occurred. Please try again.',
      privacyNote: "This page ONLY collects the answers choices and the handle you choose. The handle is (only) for you to view the results later, the answer choices are used to calculate stats.",
    },
    resultsView:{
      copySuccess: 'Copied to the clipboard',
      copyError: 'Could not copy to the clipboard',
      finishButton: 'Finish',
    },
    header: {
      title: 'Backwave',
      participate: 'Participate',
      create: 'Create',
      analyze: 'Analyze',
      participatePlaceholder: 'Enter review code',
      participateButton: 'Participate',
      analyzePlaceholder: 'Enter creator code',
      analyzeButton: 'Analyze',
      errorLoadingSurvey: 'Failed to load survey. Please check the code and try again.',
      emptyCodeError: 'The code cannot be empty.',
      errorLoadingResults: 'Failed to load results. Please check the creator code and try again.',
    },
    toast: {
      surveyCreated: 'Survey created successfully!',
      surveyCreationFailed: 'Failed to create survey. Please try again.',
      copiedToClipboard: 'Copied to clipboard!',
      copyFailed: 'Failed to copy to clipboard',
      // Add more toast messages as needed
    },
  };