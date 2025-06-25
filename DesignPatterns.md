Builder

# Các Design Pattern phổ biến trong Unity
## 1. Singleton Pattern
- Mục đích : Đảm bảo một class chỉ có một instance duy nhất và cung cấp điểm truy cập toàn cục đến instance đó.
- Ứng dụng : GameManager, AudioManager, ScoreManager
- Cách triển khai :
```Csharp
public class GameManager : MonoBehaviour
{
    private static GameManager instance;
    public static GameManager Instance
    {
        get { return instance; }
    }

    void Awake()
    {
        if (instance != null && instance != this)
        {
            Destroy(gameObject);
            return;
        }
        instance = this;
        DontDestroyOnLoad(gameObject);
    }
}
```
## 2. Observer Pattern
- Mục đích : Định nghĩa mối quan hệ 1-nhiều giữa các đối tượng, khi một đối tượng thay đổi trạng thái, tất cả phụ thuộc của nó được thông báo và cập nhật tự động.
- Ứng dụng : Hệ thống Event, UI Updates, Achievement System
- Cách triển khai :
```
// Subject (Publisher)
public class ScoreManager
{
    public delegate void ScoreChangeHandler(int newScore);
    public event ScoreChangeHandler OnScoreChanged;

    private int score;
    public int Score
    {
        get { return score; }
        set
        {
            score = value;
            OnScoreChanged?.Invoke(score);
        }
    }
}

// Observer (Subscriber)
public class UIManager : MonoBehaviour
{
    private ScoreManager scoreManager;

    void Start()
    {
        scoreManager.OnScoreChanged += UpdateScoreUI;
    }

    void UpdateScoreUI(int newScore)
    {
        // Cập nhật UI
    }
}
```
## 3. Object Pool Pattern
- Mục đích : Tái sử dụng đối tượng thay vì tạo/hủy liên tục, cải thiện hiệu suất.
- Ứng dụng : Đạn bắn, particle effects, enemies
- Cách triển khai :
```
public class ObjectPool : MonoBehaviour
{
    public GameObject prefab;
    public int poolSize = 20;

    private List<GameObject> pool;

    void Start()
    {
        pool = new List<GameObject>();
        for (int i = 0; i < poolSize; i++)
        {
            GameObject obj = Instantiate(prefab);
            obj.SetActive(false);
            pool.Add(obj);
        }
    }

    public GameObject GetPooledObject()
    {
        for (int i = 0; i < pool.Count; i++)
        {
            if (!pool[i].activeInHierarchy)
            {
                return pool[i];
            }
        }
        return null;
    }
}
```
## 4. Command Pattern
- Mục đích : Đóng gói yêu cầu thành đối tượng, cho phép tham số hóa client với các yêu cầu khác nhau.
- Ứng dụng : Hệ thống undo/redo, input handling, ability system
- Cách triển khai :
```
public interface ICommand
{
    void Execute();
    void Undo();
}

public class MoveCommand : ICommand
{
    private Transform transform;
    private Vector3 direction;
    private Vector3 oldPosition;

    public MoveCommand(Transform transform, Vector3 direction)
    {
        this.transform = transform;
        this.direction = direction;
    }

    public void Execute()
    {
        oldPosition = transform.position;
        transform.Translate(direction);
    }

    public void Undo()
    {
        transform.position = oldPosition;
    }
}
```
## 5. State Pattern
- Mục đích : Cho phép một đối tượng thay đổi hành vi khi trạng thái nội bộ của nó thay đổi.
- Ứng dụng : AI behavior, character states, game states
- Cách triển khai :
```
public interface IState
{
    void Enter();
    void Update();
    void Exit();
}

public class IdleState : IState
{
    private Enemy enemy;

    public IdleState(Enemy enemy)
    {
        this.enemy = enemy;
    }

    public void Enter()
    {
        // Bắt đầu animation idle
    }

    public void Update()
    {
        // Kiểm tra điều kiện chuyển state
    }

    public void Exit()
    {
        // Dọn dẹp trước khi chuyển state
    }
}
```
## Lời khuyên khi sử dụng Design Patterns
1. Không lạm dụng : Chỉ sử dụng pattern khi thực sự cần thiết
2. Hiểu rõ vấn đề : Chọn pattern phù hợp với vấn đề cần giải quyết
3. Keep It Simple : Đôi khi giải pháp đơn giản tốt hơn pattern phức tạp
4. Dễ bảo trì : Pattern nên làm code dễ bảo trì hơn, không phức tạp hóa
5. Tài liệu hóa : Comment và document rõ ràng việc sử dụng pattern
