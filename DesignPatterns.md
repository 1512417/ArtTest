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
```Csharp
// GameManager.cs
public class GameManager : MonoBehaviour
{
    private static GameManager instance;
    public static GameManager Instance => instance;

    public int score;
    public int highScore;
    public bool isPaused;

    void Awake()
    {
        if (instance != null && instance != this)
        {
            Destroy(gameObject);
            return;
        }
        instance = this;
        DontDestroyOnLoad(gameObject);
    }

    public void PauseGame()
    {
        isPaused = true;
        Time.timeScale = 0;
    }

    public void ResumeGame()
    {
        isPaused = false;
        Time.timeScale = 1;
    }
}

// Sử dụng trong các script khác
public class PlayerController : MonoBehaviour
{
    void Update()
    {
        if (GameManager.Instance.isPaused)
            return;

        // Logic xử lý player
    }
}
```
## 2. Observer Pattern
- Mục đích : Định nghĩa mối quan hệ 1-nhiều giữa các đối tượng, khi một đối tượng thay đổi trạng thái, tất cả phụ thuộc của nó được thông báo và cập nhật tự động.
- Ứng dụng : Hệ thống Event, UI Updates, Achievement System
- Cách triển khai :
```Csharp
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
```Csharp
// AchievementSystem.cs
public class AchievementSystem : MonoBehaviour
{
    public delegate void ScoreReachedHandler(int score);
    public static event ScoreReachedHandler OnScoreReached;

    private void Update()
    {
        int currentScore = GameManager.Instance.score;
        if (currentScore >= 1000)
        {
            OnScoreReached?.Invoke(currentScore);
        }
    }
}

// AchievementUnlocker.cs
public class AchievementUnlocker : MonoBehaviour
{
    void OnEnable()
    {
        AchievementSystem.OnScoreReached += UnlockScoreAchievement;
    }

    void OnDisable()
    {
        AchievementSystem.OnScoreReached -= UnlockScoreAchievement;
    }

    void UnlockScoreAchievement(int score)
    {
        Debug.Log($"Đạt thành tích: Đạt {score} điểm!");
        // Hiển thị UI thành tích
    }
}
```
## 3. Object Pool Pattern
- Mục đích : Tái sử dụng đối tượng thay vì tạo/hủy liên tục, cải thiện hiệu suất.
- Ứng dụng : Đạn bắn, particle effects, enemies
- Cách triển khai :
```Csharp
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
```Csharp
// BulletPool.cs
public class BulletPool : MonoBehaviour
{
    public static BulletPool Instance;
    public GameObject bulletPrefab;
    public int poolSize = 30;

    private List<GameObject> bullets;

    void Awake()
    {
        Instance = this;
        bullets = new List<GameObject>();

        for (int i = 0; i < poolSize; i++)
        {
            GameObject bullet = Instantiate(bulletPrefab);
            bullet.SetActive(false);
            bullets.Add(bullet);
        }
    }

    public GameObject GetBullet()
    {
        foreach (GameObject bullet in bullets)
        {
            if (!bullet.activeInHierarchy)
            {
                bullet.SetActive(true);
                return bullet;
            }
        }
        return null;
    }
}

// Weapon.cs
public class Weapon : MonoBehaviour
{
    public void Shoot()
    {
        GameObject bullet = BulletPool.Instance.GetBullet();
        if (bullet != null)
        {
            bullet.transform.position = transform.position;
            bullet.transform.rotation = transform.rotation;
        }
    }
}
```
## 4. Command Pattern
- Mục đích : Đóng gói yêu cầu thành đối tượng, cho phép tham số hóa client với các yêu cầu khác nhau.
- Ứng dụng : Hệ thống undo/redo, input handling, ability system
- Cách triển khai :
```Csharp
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
```Csharp
// Command Interface và các lệnh cụ thể
public interface ICommand
{
    void Execute();
    void Undo();
}

public class JumpCommand : ICommand
{
    private PlayerController player;
    private float jumpForce;
    private Vector3 previousPosition;

    public JumpCommand(PlayerController player, float jumpForce)
    {
        this.player = player;
        this.jumpForce = jumpForce;
    }

    public void Execute()
    {
        previousPosition = player.transform.position;
        player.Jump(jumpForce);
    }

    public void Undo()
    {
        player.transform.position = previousPosition;
    }
}

// InputHandler.cs
public class InputHandler : MonoBehaviour
{
    private PlayerController player;
    private Stack<ICommand> commandHistory;

    void Start()
    {
        player = GetComponent<PlayerController>();
        commandHistory = new Stack<ICommand>();
    }

    void Update()
    {
        if (Input.GetKeyDown(KeyCode.Space))
        {
            ICommand jumpCommand = new JumpCommand(player, 5f);
            jumpCommand.Execute();
            commandHistory.Push(jumpCommand);
        }

        if (Input.GetKeyDown(KeyCode.Z))
        {
            if (commandHistory.Count > 0)
            {
                ICommand lastCommand = commandHistory.Pop();
                lastCommand.Undo();
            }
        }
    }
}
```
## 5. State Pattern
- Mục đích : Cho phép một đối tượng thay đổi hành vi khi trạng thái nội bộ của nó thay đổi.
- Ứng dụng : AI behavior, character states, game states
- Cách triển khai :
```Csharp
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
```Csharp
// Các trạng thái
public interface IEnemyState
{
    void EnterState(Enemy enemy);
    void UpdateState(Enemy enemy);
    void ExitState(Enemy enemy);
}

public class PatrolState : IEnemyState
{
    private Vector3[] patrolPoints;
    private int currentPoint;

    public void EnterState(Enemy enemy)
    {
        Debug.Log("Bắt đầu tuần tra");
        currentPoint = 0;
    }

    public void UpdateState(Enemy enemy)
    {
        // Di chuyển giữa các điểm tuần tra
        Vector3 target = patrolPoints[currentPoint];
        enemy.MoveTo(target);

        if (Vector3.Distance(enemy.transform.position, target) < 0.1f)
        {
            currentPoint = (currentPoint + 1) % patrolPoints.Length;
        }

        // Kiểm tra phát hiện player
        if (enemy.DetectPlayer())
        {
            enemy.ChangeState(new ChaseState());
        }
    }

    public void ExitState(Enemy enemy)
    {
        Debug.Log("Kết thúc tuần tra");
    }
}

public class ChaseState : IEnemyState
{
    public void EnterState(Enemy enemy)
    {
        Debug.Log("Bắt đầu truy đuổi");
    }

    public void UpdateState(Enemy enemy)
    {
        // Truy đuổi player
        Transform player = enemy.GetPlayerTransform();
        if (player != null)
        {
            enemy.MoveTo(player.position);
        }

        // Mất dấu player
        if (!enemy.DetectPlayer())
        {
            enemy.ChangeState(new PatrolState());
        }
    }

    public void ExitState(Enemy enemy)
    {
        Debug.Log("Kết thúc truy đuổi");
    }
}

// Enemy.cs
public class Enemy : MonoBehaviour
{
    private IEnemyState currentState;
    private Transform player;
    public float moveSpeed = 5f;
    public float detectionRange = 10f;

    void Start()
    {
        ChangeState(new PatrolState());
    }

    void Update()
    {
        currentState?.UpdateState(this);
    }

    public void ChangeState(IEnemyState newState)
    {
        currentState?.ExitState(this);
        currentState = newState;
        currentState.EnterState(this);
    }

    public void MoveTo(Vector3 position)
    {
        transform.position = Vector3.MoveTowards(
            transform.position,
            position,
            moveSpeed * Time.deltaTime
        );
    }

    public bool DetectPlayer()
    {
        return Vector3.Distance(transform.position, player.position) < detectionRange;
    }

    public Transform GetPlayerTransform()
    {
        return player;
    }
}
```
## Lời khuyên khi sử dụng Design Patterns
1. Không lạm dụng : Chỉ sử dụng pattern khi thực sự cần thiết
2. Hiểu rõ vấn đề : Chọn pattern phù hợp với vấn đề cần giải quyết
3. Keep It Simple : Đôi khi giải pháp đơn giản tốt hơn pattern phức tạp
4. Dễ bảo trì : Pattern nên làm code dễ bảo trì hơn, không phức tạp hóa
5. Tài liệu hóa : Comment và document rõ ràng việc sử dụng pattern
