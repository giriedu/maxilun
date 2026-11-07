using System;
using System.ComponentModel;
using System.Runtime.CompilerServices;
using System.Threading.Tasks;
using System.Windows.Input;

namespace MaxilunDesktop.ViewModels
{
    public class RelayCommand : ICommand
    {
        private readonly Action _execute;
        private readonly Func<bool> _canExecute;

        public RelayCommand(Action execute, Func<bool> canExecute = null)
        {
            _execute = execute ?? throw new ArgumentNullException(nameof(execute));
            _canExecute = canExecute;
        }

        public event EventHandler CanExecuteChanged
        {
            add => CommandManager.RequerySuggested += value;
            remove => CommandManager.RequerySuggested -= value;
        }

        public bool CanExecute(object parameter) => _canExecute == null || _canExecute();
        public void Execute(object parameter) => _execute();
    }

    public class MainViewModel : INotifyPropertyChanged
    {
        private string _statusText = "Transaction buffer ready. Press Sync to commit.";
        private string _footerStatus = "Connected to SQLCA Database | Isolation: ReadCommitted";
        private bool _isBusy;

        public event PropertyChangedEventHandler PropertyChanged;

        public string StatusText
        {
            get => _statusText;
            set { _statusText = value; OnPropertyChanged(); }
        }

        public string FooterStatus
        {
            get => _footerStatus;
            set { _footerStatus = value; OnPropertyChanged(); }
        }

        public ICommand SyncCommand { get; }

        public MainViewModel()
        {
            SyncCommand = new RelayCommand(async () => await ExecuteSyncAsync(), () => !_isBusy);
        }

        private async Task ExecuteSyncAsync()
        {
            _isBusy = true;
            StatusText = "Synchronizing DataWindow buffer with remote database...";
            CommandManager.InvalidateRequerySuggested();

            try
            {
                // Non-blocking asynchronous I/O simulation
                await Task.Delay(1000);
                StatusText = "Buffer committed successfully. 0 uncommitted changes.";
                FooterStatus = $"Last commit: {DateTime.Now:HH:mm:ss} | Invariants verified";
            }
            finally
            {
                _isBusy = false;
                CommandManager.InvalidateRequerySuggested();
            }
        }

        protected void OnPropertyChanged([CallerMemberName] string propertyName = null)
        {
            PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(propertyName));
        }
    }
}
