import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay, classification_report

def plot_confusion_matrix(y_test, y_pred, labels):
    """Plot confusion matrix."""
    cm = confusion_matrix(y_test, y_pred)
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=labels)
    disp.plot(cmap=plt.cm.Blues)
    plt.show()

def plot_classification_report(y_test, y_pred):
    """Plot a visual classification report."""
    report = classification_report(y_test, y_pred, output_dict=True)
    categories = list(report.keys())[:-3]  # Remove 'accuracy', 'macro avg', and 'weighted avg'
    f1_scores = [report[cat]['f1-score'] for cat in categories]
    
    plt.figure(figsize=(10, 5))
    plt.bar(categories, f1_scores, color='skyblue')
    plt.xlabel('Classes')
    plt.ylabel('F1 Score')
    plt.title('F1 Score for Each Class')
    plt.show()




# # Inside src/visualize.py
# from sklearn.metrics import classification_report

# y_pred = model.predict(X_test)
# plot_classification_report(y_test, y_pred)


# plot_confusion_matrix(y_test, y_pred, labels=['food', 'shelter', 'material', 'location', 'medicine', 'disease'])
