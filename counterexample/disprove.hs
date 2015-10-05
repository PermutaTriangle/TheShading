import qualified Data.Set as Set
import Data.List
import System.Random

type Permutation = [Int]
type Pattern = [Int]
type MeshPattern = ([Int], Set.Set (Int,Int))

flatten :: [Int] -> Permutation
flatten xs = map snd $ sort $ [ (j,i) | (i,(_,j)) <- zip [1..] $ sort $ zip xs [1..] ]

-- containment :: Pattern -> Permutation -> [[Int]]
-- containment patt perm =
--         filter ok $ doit (length patt) [] perm
--     where
--         ok sub = patt == (flatten sub)
--         doit 0 sub _ = sub
--         doit k 

containment [] _ = [[]]
containment _ [] = []
containment (x:xs) (y:ys) =
        iter (containment (x:xs) ys) (containment xs ys)
    where
        flat = flatten (x:xs)
        iter [] [] = []
        iter [] (p:ps)
            | flatten (y:p) == flat = (y:p) : (iter [] ps)
            | otherwise             = iter [] ps
        iter (q:qs) ps = q : (iter qs ps)

randomPermutation :: RandomGen rg => Int -> rg -> (Permutation, rg)
randomPermutation 0 g = ([], g)
randomPermutation n g =
        (perm', g'')
    where
        (perm, g') = randomPermutation (n-1) g
        (p, g'') = randomR (1, n) g'
        perm' = p:[ if q < p then q else q+1 | q <- perm ]


main = do
    g <- getStdGen
    let (perm, gp) = randomPermutation 20 g
    -- putStrLn $ show $ perm
    -- putStrLn $ show $ flatten [9,2,8,4]
    -- let perm = [2,5,6,3,1,4]
    -- putStrLn $ show perm
    mapM_ (putStrLn . show) $ containment [2,3,1] perm
    -- putStrLn "Hello World!"
    -- mapM_ (putStrLn . show) $ containment [1,2] [2,5,6,3,1,4]
    -- putStrLn "Hello Worldz!"

